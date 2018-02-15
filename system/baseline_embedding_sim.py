import sys
from embeddings import load_model, sim_wv, check_vocab
from utils import load_triples, results_to_file, decisions_to_file
import os

def sim_check(concept1, concept2, prop, model):

    decision_dict = dict()
    decision_dict['system'] = 'sim'

    if check_vocab([concept1, concept2, prop], model):
        #sim1, sim2 = embedding_sim(concept1, concept2, prop, model)
        sim1 = sim_wv(concept1, prop, model)
        sim2 = sim_wv(concept2, prop, model)


        if sim1 > sim2:
            decision_dict['answer'] = '1'
        else:
            decision_dict['answer'] = '0'
    else:
        decision_dict['answer'] = '0'

    return decision_dict


def embedding_baseline(data, model):

    triples = load_triples(data)
    answers = []
    name = 'baseline_sim_'+data


    for triple in triples:
        concept1 = triple[0]
        concept2 = triple[1]
        prop = triple[2]

        decision_dict = sim_check(concept1, concept2, prop, model)

        answers.append(decision_dict['answer'])

    print('len data ', len(triples))
    print('len answers ', len(answers))
    results_to_file(triples, answers, name)


if __name__ == '__main__':

    data = sys.argv[1]

    if not os.path.isdir('../results'):
        os.mkdir('../results')

    # replace this with the path to your the word2vec model
    #model_path = '../model/movies.bin'
    model_path = '../../../Data/word2vec/GoogleNews-vectors-negative300.bin'
    model = load_model(model_path)


    embedding_baseline(data, model)
