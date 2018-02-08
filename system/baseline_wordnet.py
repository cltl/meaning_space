from wordnet import get_all_definitions
from wordnet import get_all_synsets
from wordnet import get_syn_depth, get_syns_depths
from utils import load_triples, results_to_file



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

    decision_dict['depths_concept1'] = get_syns_depths(syns_concept1)
    decision_dict['level'] = '-'
    decision_dict['decision_depth'] = '-'

    for syn1, def1 in def_dict1.items():

        if prop in def1:
            def1_answer = 1
            decision_dict['decision_depth'] = get_syn_depth(syn1)

            # Check the level at which the decision is made:
            if syn1 in syns_concept1:
                decision_dict['level'] = 'synset'
            else:
                decision_dict['level'] = 'hypernym'
            break

    for syn2, def2 in def_dict2.items():
        if prop in def2:
            def2_answer = 1
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
    name = 'def_baseline_'+data


    for triple in triples:
        concept1 = triple[0]
        concept2 = triple[1]
        prop = triple[2]

        def_answer = None

        def_decision_dict = direct_def_check(concept1, concept2, prop)
        def_answer = def_decision_dict['answer']

        if def_answer:
            answers.append(def_answer)
        else:
            answers.append('0')


    print('len data ', len(triples))
    print('len answers ', len(answers))
    results_to_file(triples, answers, name)
