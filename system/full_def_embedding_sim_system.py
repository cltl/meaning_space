import sys
from embeddings import load_model, sim_wv, highest_sim_word_list
from utils import load_triples, results_to_file, decisions_to_file
from wordnet import get_all_definitions
from baseline_wordnet import direct_def_check
from definitions_extended_system import sim_def_check
from baseline_embedding_sim import sim_check
import os

def full_def_embedding_sim_system(data, threshold1, threshold2, model):


    triples = load_triples(data)
    answers = []
    decision_dicts = []
    name = 'full_def_embedding_sim_system_'+str(threshold1)+'-'+str(threshold2)+'_'+data


    for triple in triples:
        concept1 = triple[0]
        concept2 = triple[1]
        prop = triple[2]

        def_answer = None
        def_sim_answer = None
        sim_answer = None

        def_decision_dict = direct_def_check(concept1, concept2, prop)
        def_sim_decision_dict = sim_def_check(concept1, concept2, prop, threshold1, threshold2, model)
        def_answer = def_decision_dict['answer']
        def_sim_answer = def_sim_decision_dict['answer']



        if def_answer != None:
            print(def_answer)
            answers.append(def_answer)
            decision_dicts.append(def_decision_dict)
        elif def_sim_answer != None:
            answers.append(def_sim_answer)
            decision_dicts.append(def_sim_decision_dict)
        else:
            sim_decision_dict = sim_check(concept1, concept2, prop, model)
            sim_answer = sim_decision_dict['answer']
            decision_dicts.append(sim_decision_dict)


    print('len data ', len(triples))
    print('len answers ', len(answers))
    results_to_file(triples, answers, name)
    decisions_to_file(triples, decision_dicts, name)



if __name__ == '__main__':

    data = sys.argv[1]

    if not os.path.isdir('../results'):
        os.mkdir('../results')

    # replace this with the path to your the word2vec model
    model_path = '../model/movies.bin'
    model = load_model(model_path)


    threshold1 = 0.75
    threshold2 = 0.23

    full_def_embedding_sim_system(data, threshold1, threshold2, model)
