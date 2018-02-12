from collections import defaultdict
from collections import Counter
import glob
import sys
import os


def load_data(system_path, gold_path):

    with open(system_path) as infile:
        system = [line.split(',') for line in infile.read().strip().split('\n')]

    with open(gold_path) as infile:
        gold = [line.split(',') for line in infile.read().strip().split('\n')]

    system_triples = [triple[:3] for triple in system]
    gold_triples = [triple[:3] for triple in gold]

    for n, system_triple in enumerate(system_triples):
        if system_triple not in gold_triples:
            print(n, 'not in gold: ',system_triple)


    for gold_triple in gold_triples:
        if gold_triple not in system_triples:
            print('not in system: ',gold_triple)

    #assert system_triples == gold_triples, "System triples differ from gold triples"

    return system, gold


def count_examples_and_properties(gold):

    props = set([triple[2] for triple in gold])

    return len(gold), len(props)


def load_annotations(annotation_path):

    with open(annotation_path) as infile:
        lines = [line.split('\t') for line in infile.read().strip().split('\n')]

    annotation_dict = dict()

    for line in lines:
        annotation = '-'.join(sorted([word.strip() for word in line[1:]]))
        word = line[0]

        annotation_dict[word] = annotation


    return annotation_dict

def get_cases_per_category(system, gold, annotation_dict):

    # Sanity check: length of system

    props_gold = set([triple[2] for triple in gold])
    props_system = set([triple[2] for triple in system])

    assert len(props_gold) == len(props_system) #== len(annotation_dict.keys()), 'annotations don t match data'

    line_counter = 0
    category_dict = defaultdict(list)

    for line_system, line_gold in zip(system, gold):
        line_counter +=1

        label_system = line_system[3]
        label_gold = line_gold[3]

        prop = line_system[2].strip('?')
        category = annotation_dict[prop]


        if line_system[3] == line_gold[3] == '1':
            label = 'tp'
            category_dict[category].append( label)
        elif line_system[3] == line_gold[3] == '0':
            label = 'tn'

            category_dict[category].append(label)

        elif line_system[3] != line_gold[3] == '0':
            label = 'fp'
            category_dict[category].append(label)

        elif line_system[3] != line_gold[3] == '1':
            label = 'fn'
            category_dict[category].append(label)

    # Sanity check: are all cases categorized?
    cases = []
    for cat, case_list in category_dict.items():
        for case in case_list:
            cases.append(case)
    assert len(cases) == line_counter, 'Not all triples categorized'

    return category_dict

def get_cases_per_cat_relation(system, gold, annotation_dict_pro, annotation_dict_concept):
    pass


    return category_dict

def find_cases(category, system_path, data):

    annotation_path = '../attribute_annotation/attributes-validation.txt'

    annotation_dict = load_annotations(annotation_path)

    system, gold = load_data(system_path, '../data/'+data+'.txt')

    target_cases = []

    for prop, annotation in annotation_dict.items():

        if annotation == category:
            for case in system:
                if case[2] == prop:
                    target_cases.append(case)

    return target_cases




def cateogry_cases_to_file(gold_path, system_path, annotations_path, error_analysis_path):

    system, gold = load_data(system_path, gold_path)

    annotation_dict = load_annotations(annotations_path)

    category_dict = get_cases_per_category(system, gold, annotation_dict)

    category_evaluation_dict = dict()

    with open(error_analysis_path, 'w') as outfile:

        outfile.write('category,tp,tn,fp,fn,sum-cases,precision,recall,f1-positive,f1-average\n')


        for category, case_list in category_dict.items():


            case_counter = Counter(case_list)

            tp = case_counter['tp']
            tn = case_counter['tn']
            fp = case_counter['fp']
            fn = case_counter['fn']


            precision_positive = 0
            recall_positive = 0
            f1_positive = 0

            precision_negative = 0
            recall_negative = 0
            f1_negative = 0

            if tp > 0:
                precision_positive = float(tp)/(tp+fp)
                recall_positive =float(tp)/(tp+fn)
                f1_positive = 2*((precision_positive*recall_positive)/(precision_positive+recall_positive))


            if tn > 0:
                precision_negative = float(tn)/(tn+fn)
                recall_negative = float(tn)/(tn+fp)
                f1_negative = 2*((precision_negative * recall_negative)/(precision_negative + recall_negative))

            if f1_positive and f1_negative:
                f1_average = (f1_positive+f1_negative)/2.0
            else:
                precision_positive = 0
                precision_negative = 0
                recall_positive = 0
                recall_negative = 0
                f1_positive = 0
                f1_average = 0


            line = [tp, tn, fp, fn, sum([tp, tn, fp, fn]), precision_positive, recall_positive, f1_positive, f1_average]

            line_str = [str(item) for item in line]

            outfile.write(category+','+','.join(line_str)+'\n')

def evaluate_per_category(system_paths, gold_path, data):

    if not os.path.isdir('categories'):
        os.mkdir('categories')

    for system_path in system_paths:
        print(system_path)
        error_analysis_path = 'categories/cat_'+system_name+'.txt'

        cateogry_cases_to_file(gold_path, system_path, annotations_path, error_analysis_path)




if __name__ == '__main__':


    data = sys.argv[1]

    gold_path = '../data/'+data+'.txt'
    system_paths = glob.glob('../results/*.txt')
    annotations_path = '../attribute_annotation/attributes-validation.txt'

    evaluate_per_category(system_paths, gold_path, data)
