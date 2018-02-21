from wordnet import get_all_definitions
from wordnet import get_all_synsets, check_if_syn_in_hyponyms
from wordnet import get_syn_depth, get_syns_depths, get_all_meronyms
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


    for syn1, def1 in def_dict1.items():

        if prop in def1:

            def1_answer = 1
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
    decision_dict['system'] = 'def'

    return decision_dict

def direct_def_check_record_decisions(concept1, concept2, prop):

    """
    Input: concept1 (str), concept2 (str)
    Output: Either a decisions (str '1' or '0') or None
    Checks whether the attribute is in any of the definitions of concept1 and
    concept2
    """

    decision_dict = dict()

    def_dict1 = get_all_definitions(concept1)
    def_dict2 = get_all_definitions(concept2)

    syns1 = get_all_synsets(concept1)
    syns2 = get_all_synsets(concept2)

    def1_answer = 0
    def2_answer = 0

    decision_dict['concept1_syns'] = ' '.join([str(syn) for syn in syns1])
    decision_dict['concept2_syns'] = ' '.join([str(syn) for syn in syns2])

    decision_dict['decision1_syn'] = '-'
    decision_dict['decision2_syn'] = '-'
    decision_dict['system'] = 'def'

    for syn1, def1 in def_dict1.items():

        if prop in def1:

            def1_answer = 1
            decision_dict['decision1_syn'] = str(syn1)
            break

    for syn2, def2 in def_dict2.items():
        if prop in def2:
            def2_answer = 1
            decision_dict['decision2_syn'] = str(syn2)
            break


    if (def1_answer == 1) and (def2_answer == 0):
        answer = '1'

    elif (def1_answer == 1) and (def2_answer == 1):
        answer = '0'

    elif (def1_answer == 0) and (def2_answer == 1):
        answer = '0'

    else:
        answer = None
        decision_dict['system'] = '-'

    decision_dict['answer'] = answer


    return decision_dict

def direct_part_check(concept1, concept2, prop):

    """
    Input: concept1 (str), concept2 (str)
    Output: Either a decisions (str '1' or '0') or None
    Checks whether the attribute is in any of the parts of concept1 and
    concept2
    """

    decision_dict = dict()

    part_dict1 = get_all_meronyms(concept1)
    part_dict2 = get_all_meronyms(concept2)

    part1_answer = 0
    part2_answer = 0


    for syn1, part1 in part_dict1.items():

        if prop in part1:

            part1_answer = 1
            break

    for syn2, part2 in part_dict2.items():
        if prop in part2:
            part2_answer = 1
            break


    if (part1_answer == 1) and (part2_answer == 0):
        answer = '1'

    elif (part1_answer == 1) and (part2_answer == 1):
        answer = '0'

    elif (part1_answer == 0) and (part2_answer == 1):
        answer = '0'

    else:
        answer = None

    decision_dict['answer'] = answer
    decision_dict['system'] = 'part'

    return decision_dict


def def_baseline(data):


    triples = load_triples(data)
    answers = []
    decision_dicts = []
    name = 'baseline_definitions_'+data


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
            def_decision_dict['system'] = 'def'
        else:
            answers.append('0')


    print('len data ', len(triples))
    print('len answers ', len(answers))
    results_to_file(triples, answers, name)


def def_baseline_record_decisions(data):


    triples = load_triples(data)
    answers = []
    decision_dicts = []
    name = 'baseline_definitions_'+data


    for triple in triples:
        concept1 = triple[0]
        concept2 = triple[1]
        prop = triple[2]

        def_answer = None

        def_decision_dict = direct_def_check_record_decisions(concept1, concept2, prop)
        decision_dicts.append(def_decision_dict)
        def_answer = def_decision_dict['answer']

        if def_answer:
            answers.append(def_answer)
            def_decision_dict['system'] = 'def'
        else:
            answers.append('0')
            def_decision_dict['system'] = '-'


    print('len data ', len(triples))
    print('len answers ', len(answers))
    results_to_file(triples, answers, name)
    decisions_to_file(triples, decision_dicts, name)

def part_baseline(data):


    triples = load_triples(data)
    answers = []
    decision_dicts = []
    name = 'baseline_parts_'+data


    for triple in triples:
        concept1 = triple[0]
        concept2 = triple[1]
        prop = triple[2]

        part_answer = None

        part_decision_dict = direct_part_check(concept1, concept2, prop)
        decision_dicts.append(part_decision_dict)
        part_answer = part_decision_dict['answer']

        if part_answer:
            answers.append(part_answer)
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

    def_baseline_record_decisions(data)
    #def_baseline(data)
    #part_baseline(data)
