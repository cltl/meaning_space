from nltk.corpus import wordnet as wn
from collections import defaultdict
from collections import Counter
import sys

def load_synset(syn_str):

    name = syn_str.split("'")[1]

    syn = wn.synset(name)

    return syn


def load_decisions(filepath):

    decision_dict = defaultdict(list)

    with open(filepath) as infile:
        lines = infile.read().strip().split('\n')

    headers = lines[0].split(',')


    for line in lines[1:]:
        line_list = line.split(',')
        for header, value in zip(headers, line_list):
            decision_dict[header].append(value)

    return decision_dict




def get_levels_and_counts(decision_dict, name1, name2):

    depth_list = [] # depth concept1_syn, depth_decision_syn, difference

    level_counter = Counter()
    level_counter['overall'] = 0
    level_counter['wordnet_decisions'] = 0
    level_counter['same_syn'] = 0
    level_counter['hypernym'] = 0

    depth_diffs = []


    for c_syn, d_syn in zip(decision_dict[name1], decision_dict[name2]):

        level_counter['overall'] += 1


        if (c_syn != '-') and (d_syn != '-'):

            level_counter['wordnet_decisions'] += 1
            c_depth = load_synset(c_syn).max_depth()
            d_depth = load_synset(d_syn).max_depth()

            if (c_depth == d_depth):
                level_counter['same_syn'] += 1

            elif (c_depth != d_depth):
                level_counter['hypernym'] += 1
                diff = c_depth - d_depth
                depth_diffs.append(diff)
        else:
            c_depth = '-'
            d_depth = '-'
            diff = '-'

        depth_list.append((c_depth, d_depth, diff))

    level_counter['depth_diff_sum'] = sum(depth_diffs)

    return depth_list, level_counter





def analyze_distinction_levels(system_name):

    filepath = '../results/decisions/'+system_name+'.txt'

    decision_dict = load_decisions(filepath)

    concept1_depths, level_counter1 = get_levels_and_counts(decision_dict, 'concept1_syn', 'decision1_syn')
    concept2_depths, level_counter2 = get_levels_and_counts(decision_dict, 'concept2_syn', 'decision2_syn')

    concepts1 = decision_dict['concept1']
    concepts2 = decision_dict['concept2']
    attributes = decision_dict['attribute']

    overall_stats = level_counter1 + level_counter2
    overall_stats['average_depth_difference'] = overall_stats['depth_diff_sum'] / overall_stats['hypernym']


    print(len(concepts1), len(concepts2), len(attributes))

    with open('wordnet_distinction_level/'+system_name+'.txt', 'w') as outfile:

        outfile.write('concept1,concept2,attribute,concept1_depth,decision1_depth,difference1,concept2_depth,decision2_depth,difference2\n')

        for c1, c2, a, c1d, c2d in zip(concepts1, concepts2, attributes, concept1_depths, concept2_depths):

            c1d_str = ','.join([str(v) for v in c1d])
            c2d_str = ','.join([str(v) for v in c2d])
            triple_str = ','.join([c1, c2, a])

            outfile.write(triple_str+','+c1d_str+','+c2d_str+'\n')
    # Write stats to file
    with open('wordnet_distinction_level/stats_'+system_name+'.txt', 'w') as outfile:
        for k, v in overall_stats.items():
            outfile.write(k+','+str(v)+'\n')




if __name__ == '__main__':

    system_name = sys.argv[1]

    analyze_distinction_levels(system_name)
