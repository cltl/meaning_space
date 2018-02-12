from wordnet import get_all_definitions
from wordnet import get_all_synsets, check_if_syn_in_hyponyms
from wordnet import get_syn_depth, get_syns_depths
from utils import load_triples, results_to_file, decisions_to_file
import os
import sys


def direct_def_check(concept1, concept2, prop):

    """
    Input: concept1 (str), concept2 (str)
    Output: Either a decisions (str '1' or '0') or None
    Checks whether the attribute is in any of the definitions of concept1 and
    concept2
    """

    decision_dict = dict()

    def_dict1 = get_all_definitions(concept1)
    def_dict2 = get_all_definitions(concept2)

    def1_answer = 0
    def2_answer = 0

    syns_concept1 = get_all_synsets(concept1)
    syns_concept2 = get_all_synsets(concept2)


    decision_dict['decision1_syn'] = '-'
    decision_dict['decision2_syn'] = '-'
    decision_dict['concept1_syn'] = '-'
    decision_dict['concept2_syn'] = '-'
    decision_dict['system'] = 'def'

    for syn1, def1 in def_dict1.items():

        if prop in def1:

            def1_answer = 1
            decision_dict['decision1_syn'] = str(syn1)

            # check if the decision was taken at the level of the synsets of concept1
            # this is the case, if the decision synsets is one of the syns of concept1
            # in this case, it is not necessary to find the hyponym of the decision synset
            # in order to calculate the depth difference later
            if syn1 in syns_concept1:
                decision_dict['concept1_syn'] = str(syn1)

                break
            else:
                for syn_concept1 in syns_concept1:
                    if check_if_syn_in_hyponyms(syn_concept1, syn1):
                        decision_dict['concept1_syn'] = str(syn_concept1)
                        break
                    else:
                        decision_dict['concept1_syn'] = 'pos_dec_syn_is_'+str(syn1.pos())



    for syn2, def2 in def_dict2.items():
        if prop in def2:
            def2_answer = 1
            decision_dict['decision2_syn'] = str(syn2)

            decision_dict['decision2_syn'] = str(syn2)
            # check if the decision was taken at the level of the synsets of concept1
            # this is the case, if the decision synsets is one of the syns of concept1
            # in this case, it is not necessary to find the hyponym of the decision synset
            # in order to calculate the depth difference later
            if syn2 in syns_concept2:
                decision_dict['concept2_syn'] = str(syn2)
                break
            else:
                for syn_concept2 in syns_concept2:
                    if check_if_syn_in_hyponyms(syn_concept2, syn2):
                        decision_dict['concept2_syn'] = str(syn_concept2)
                        break


    if (def1_answer == 1) and (def2_answer == 0):
        answer = '1'

    elif (def1_answer == 1) and (def2_answer == 1):
        answer = '0'

    elif (def1_answer == 0) and (def2_answer == 1):
        answer = '0'

    else:
        answer = None

    decision_dict['answer'] = answer

    return decision_dict


def def_baseline(data):


    triples = load_triples(data)
    answers = []
    decision_dicts = []
    name = 'def_baseline_'+data


    for triple in triples:
        concept1 = triple[0]
        concept2 = triple[1]
        prop = triple[2]

        def_answer = None

        def_decision_dict = direct_def_check(concept1, concept2, prop)
        decision_dicts.append(def_decision_dict)
        def_answer = def_decision_dict['answer']

        if def_answer:
            answers.append(def_answer)
        else:
            answers.append('0')


    print('len data ', len(triples))
    print('len answers ', len(answers))
    results_to_file(triples, answers, name)
    decisions_to_file(triples, decision_dicts, name)

if __name__ == '__main__':

    if not os.path.isdir('../results'):
        os.mkdir('../results')


    data = sys.argv[1]


    def_baseline(data)
