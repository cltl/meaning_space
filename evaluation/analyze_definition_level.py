from nltk.corpus import wordnet as wn
from collections import defaultdict
from collections import Counter
import sys

def load_synset(syn_str):

    name_list = syn_str.split("'")

    if len(name_list) == 3:
        name = name_list[1]

        if len(name.split('.')) == 3:

            syn = wn.synset(name)
        else:
            syn = None
    else:
        syn = None

    return syn


def load_decisions(filepath):

    decision_dicts = []

    with open(filepath) as infile:
        lines = infile.read().strip().split('\n')

    headers = lines[0].split(',')


    for line in lines[1:]:
        line_list = line.split(',')
        line_dict = dict()
        for header, value in zip(headers, line_list):
            line_dict[header] = value
        decision_dicts.append(line_dict)

    return decision_dicts

def get_all_hyponyms(syn):

    all_hyponyms = []

    for hypo in syn.hyponyms():
        all_hyponyms.append(hypo)

    for hypo in all_hyponyms:
        for hypo1 in hypo.hyponyms():
            if hypo1 not in all_hyponyms:
                all_hyponyms.append(hypo1)
    return all_hyponyms

def get_levels_and_counts(decision_dicts):

    depth_list = [] # depth concept1_syn, depth_decision_syn, difference

    level_counter = Counter()
    level_counter['overall'] = 0
    level_counter['wordnet_decisions'] = 0
    level_counter['same_syn'] = 0
    level_counter['hypernym'] = 0

    depth_diffs = []


    for decision_dict in decision_dicts:

        level_counter['overall'] += 1

        if decision_dict['system'] == 'def':
            level_counter['wordnet_decisions'] += 1

            decision_syns = [decision_dict['decision1_syn'], decision_dict['decision2_syn']]
            concept1_syns = decision_dict['concept1_syns'].split(' ')
            concept2_syns = decision_dict['concept2_syns'].split(' ')

            for decision_syn in decision_syns:
                if decision_syn != '-':
                    print('\nWorking on ', decision_syn)
                    if decision_syn in concept1_syns + concept2_syns:

                        level_counter['same_syn'] += 1
                    else:
                        level_counter['hypernym'] += 1

                        # check the hight difference
                        decision_synset = load_synset(decision_syn)
                        hypos = get_all_hyponyms(decision_synset)

                        for concept_syn in concept1_syns + concept2_syns:
                            #print(concept_syn)
                            concept_syn = load_synset(concept_syn)
                            if concept_syn:
                                if concept_syn in hypos:

                                    print('found the concept synset!', concept_syn)

                                    depth_c = concept_syn.max_depth()
                                    depth_d = decision_synset.max_depth()

                                    depth_diff = depth_c - depth_d

                                    print(depth_diff)
                                    depth_diffs.append(depth_diff)

    average_depth_difference = sum(depth_diffs) / len(depth_diffs)

    return average_depth_difference, level_counter








def analyze_distinction_levels(system_name):

    filepath = '../results/decisions/'+system_name+'.txt'

    decision_dicts = load_decisions(filepath)

    av_depth_diff, level_counter = get_levels_and_counts(decision_dicts)


    print('writing results to file')
    # Write stats to file
    with open('wordnet_distinction_level/stats_'+system_name+'.txt', 'w') as outfile:
        outfile.write('av_depth_difference,'+str(av_depth_diff)+'\n')
        for k, v in level_counter.items():

            outfile.write(k+','+str(v)+'\n')




if __name__ == '__main__':

    system_name = sys.argv[1]

    analyze_distinction_levels(system_name)
