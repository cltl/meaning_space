import sys
from embeddings import load_model, sim_wv, subtract
from utils import load_triples, results_to_file, decisions_to_file
from classification import scale_training_test_features, train_classifier
from classification import test_classifier
import os

def get_sim_subtracted(concept1, concept2, prop, model):


    vec_sub = subtract(concept2, concept1, model)

    if type(vec_sub) != str:

        sim_sub = sim_wv(vec_sub, prop, model)
    else:
        sim_sub = 0.0

    return sim_sub



def extract_features(triples, model):

    features = []

    for triple in triples:
        concept1 = triple[0]
        concept2 = triple[1]
        prop = triple[2]

        features.append([get_sim_subtracted(concept1, concept2, prop, model)])

    return features


def embedding_subtraction_classification_baseline(data_train, data_test, model, hidden_layer, activation):


    hiddel_layer_str = '-'.join([str(l) for l in hidden_layer])

    name = 'embedding_sub_cl_baseline_'+hiddel_layer_str+'_'+activation+'_'+data_test

    triples_train, labels_train = load_triples(data_train, return_labels = True)
    triples_test = load_triples(data_test)

    x_train = extract_features(triples_train, model)
    x_test = extract_features(triples_test, model)

    x_train_scaled, x_test_scaled = scale_training_test_features(x_train, x_test)

    classifier = train_classifier(x_train_scaled, labels_train, hidden_layer, activation)

    predictions = test_classifier(classifier, x_train_scaled)

    results_to_file(triples_test, predictions, name)



if __name__ == '__main__':

    data_train = sys.argv[1]
    data_test = sys.argv[2]

    if not os.path.isdir('../results'):
        os.mkdir('../results')

    # replace this with the path to your the word2vec model
    #model_path = '../model/movies.bin'
    model_path = '../../../Data/word2vec/GoogleNews-vectors-negative300.bin'
    model = load_model(model_path)

    hidden_layer = (1,1)
    activation = 'logistic'


    embedding_subtraction_classification_baseline(data_train, data_test, model, hidden_layer, activation)
