import sys
from embeddings import load_model, sim_wv, highest_sim_word_list
from utils import load_triples, results_to_file, decisions_to_file
from wordnet import get_all_definitions
from baseline_wordnet import direct_def_check
from definitions_extended_system import sim_def_check
from baseline_embedding_subtraction import extract_features
from classification import scale_training_test_features, train_classifier
from classification import test_classifier



def full_def_embedding_sub_system(data_train, data_test, threshold1, threshold2, model):


    triples_train, labels_train = load_triples(data_train, return_labels = True)
    triples_test = load_triples(data_test)

    answers = []
    decision_dicts = []
    name = 'full_def_embedding_subtraction_system_'+str(threshold1)+'-'+str(threshold2)+'_'+data_test

    hidden_layer = (1,1)
    activation = 'logistic'

    x_train = extract_features(triples_train, model)
    x_test = extract_features(triples_test, model)

    x_train_scaled, x_test_scaled = scale_training_test_features(x_train, x_test)

    classifier = train_classifier(x_train_scaled, labels_train, hidden_layer, activation)

    predictions = test_classifier(classifier, x_train_scaled)



    for triple, prediction in zip(triples_test, predictions):
        concept1 = triple[0]
        concept2 = triple[1]
        prop = triple[2]

        def_answer = None
        def_sim_answer = None
        sim_answer = None

        def_decision_dict = direct_def_check(concept1, concept2, prop)
        def_sim_decision_dict = sim_def_check(concept1, concept2, prop, threshold1, threshold2, model)
        def_answer = def_decision_dict['answer']


        if def_answer != None:
            print(def_answer)
            answers.append(def_answer)
            decision_dicts.append(def_decision_dict)
        elif def_sim_answer != None:
            answers.append(def_sim_answer)
            decision_dicts.append(def_sim_decision_dict)
        else:
            sub_decision_dict = dict()
            sub_decision_dict['depths_concept1'] = '-'
            sub_decision_dict['level'] = '-'
            sub_decision_dict['decision_depth'] = '-'
            sub_decision_dict['system'] = 'sub'
            sub_decision_dict['answer'] = str(prediction)
            sub_answer = str(prediction)
            answers.append(sub_answer)
            decision_dicts.append(sub_decision_dict)


    print('len data ', len(triples_test))
    print('len answers ', len(answers))
    results_to_file(triples_test, answers, name)
    decisions_to_file(triples_test, decision_dicts, name)


if __name__ == '__main__':

    data_train = sys.argv[1]
    data_test = sys.argv[2]

    # replace this with the path to your the word2vec model
    model_path = '../model/movies.bin'
    model = load_model(model_path)


    threshold1 = 0.75
    threshold2 = 0.23

    full_def_embedding_sub_system(data_train, data_test, threshold1, threshold2, model)
