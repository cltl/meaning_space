import sys
from embeddings import load_model, sim_wv
from utils import load_triples, results_to_file, decisions_to_file


def sim_check(concept1, concept2, prop, model):

    decision_dict = dict()

    sim1 = sim_wv(concept1, prop, model)
    sim2 = sim_wv(concept1, prop, model)

    decision_dict['depths_concept1'] = '-'
    decision_dict['level'] = '-'
    decision_dict['decision_depth'] = '-'
    decision_dict['system'] = 'sim'

    if sim1 > sim2:
        decision_dict['answer'] = '1'
    else:
        decision_dict['answer'] = '0'
    return decision_dict


def embedding_baseline(data, model):

    triples = load_triples(data)
    answers = []
    name = 'embedding_sim_baseline_'+data


    for triple in triples:
        concept1 = triple[0]
        concept2 = triple[1]
        prop = triple[2]

        answer = sim_check(concept1, concept2, prop, model)

        answers.append(answer)

    print('len data ', len(triples))
    print('len answers ', len(answers))
    results_to_file(triples, answers, name)


if __name__ == '__main__':

    data = sys.argv[1]

    # replace this with the path to your the word2vec model
    model_path = '../model/movies.bin'
    model = load_model(model_path)


    embedding_baseline(data, model)
