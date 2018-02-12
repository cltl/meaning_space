from nltk.corpus import wordnet as wn
from collections import defaultdict
import sys

def load_synset(syn_str):

    name = syn_str.split("'")[1]

    syn = wn.synset(name)

    return syn


def load_decisions(filepath):

    decision_dict = defaultdict(list)

    with open(filepath) as infile:
        lines = infile.read().split('\n')

    headers = lines[0].split(',')


    for line in lines[1:]:
        line_list = line.split(',')
        for header, value in zip(headers, line_list):
            decision_dict[header].append(value)

    return decision_dict




def get_levels(decision_dict, name1, name2):

    depth_list = [] # depth concept1_syn, depth_decision_syn, difference




    for c_syn, d_syn in zip(decision_dict[name1], decision_dict[name2]):

        if c_syn != '-':
            c_depth = load_synset(c_syn).max_depth()
        else:
            c_depth = '-'
        if d_syn != '-':
            d_depth = load_synset(d_syn).max_depth()
        else: d_depth = '-'

        if (c_depth != '-') and (d_depth != '-'):
            diff = c_depth - d_depth
        else:
            diff = '-'

        depth_list.append((c_depth, d_depth, diff))

    return depth_list


def analyze_distinction_levels(system_name):

    filepath = '../results/decisions/'+system_name+'.txt'

    decision_dict = load_decisions(filepath)

    concept1_depths = get_levels(decision_dict, 'concept1_syn', 'decision1_syn')
    concept2_depths = get_levels(decision_dict, 'concept2_syn', 'decision2_syn')

    #print(concept1_depths)

    concepts1 = decision_dict['concept1']
    concepts2 = decision_dict['concept2']
    attributes = decision_dict['attribute']

    print(len(concepts1), len(concepts2), len(attributes))

    with open('wordnet_distinction_level/'+system_name+'.txt', 'w') as outfile:

        outfile.write('concept1,concept2,attribute,concept1_depth,decision1_depth,difference1,concept2_depth,decision2_depth,difference2\n')

        for c1, c2, a, c1d, c2d in zip(concepts1, concepts2, attributes, concept1_depths, concept2_depths):

            print(c1, c2, a, c1d, c2d)
            c1d_str = ','.join([str(v) for v in c1d])
            c2d_str = ','.join([str(v) for v in c2d])

            triple_str = ','.join([c1, c2, a])
            outfile.write(triple_str+','+c1d_str+','+c2d_str+'\n')


if __name__ == '__main__':

    system_name = sys.argv[1]

    analyze_distinction_levels(system_name)
