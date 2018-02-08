import os



def load_triples(data, return_labels = False):

    "Load data. Data can either be 'train', 'validation', or 'test'"

    triples = []
    labels = []

    with open('../data/'+data+'.txt') as infile:
        lines =[line.split(',') for line in infile.read().strip().split('\n')]

    for line in lines:
        if len(line) == 4:
            triples.append(line[:3])
            labels.append(int(line[3]))
        else:
            triples.append(line)
    if labels and return_labels == True:
        return triples, labels
    else:
        return triples


def results_to_file(triples_test, answers, name):

    if not os.path.isdir('../results'):
        os.mkdir('../results')

    with open('../results/'+name+'.txt', 'w') as outfile:
        for triple, answer in zip(triples_test, answers):
            outfile.write(','.join(triple)+','+str(answer)+'\n')

def error_analysis_file(triples_test, labels_test, answers, decisions, name):

    if not os.path.isdir('../error_analysis'):
        os.mkdir('../error_analysis')

    with open('../error_analysis/'+name+'.txt', 'w') as outfile:
        for triple, label, answer, decision in zip(triples_test, labels_test, answers, decisions):

            if label == 1 and answer == '1':
                case = 'tp'
            elif label == 0 and answer == '0':
                case = 'tn'
            elif label == 1 and answer == '0':
                case = 'fn'
            elif label == 0 and answer == '1':
                case = 'fp'

            outfile.write(','.join(triple)+','+decision+','+case+'\n')



def load_positive_negative_triples(data):

    with open('../DiscriminAtt/training/'+data+'.txt') as infile:

        triples = [line.split(',') for line in infile.read().strip().split('\n')]

    positive_triples = [triple[:3] for triple in triples if triple[3] == '1']
    negative_triples = [triple[:3] for triple in triples if triple[3] == '0']

    return positive_triples, negative_triples