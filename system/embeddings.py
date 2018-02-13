from gensim import models
from gensim.models import Word2Vec
import numpy as np
import math
import sys
import os


def load_model(model_path):

    """
    Load model in word2vec Google News format
    Input: path/to/model
    Output: Word2Vec model in binary format
    """

    model = models.KeyedVectors.load_word2vec_format(model_path, binary=True)
    return model




def unit_vector(vector):

    """
    Calculate unit unit_vector
    Input: vector (resulting from a calculation; vectors returned by the model are
    normalized already) (numpy array)
    Output: unit vector (numpyp array)
    """

    mag = math.sqrt(sum([pow(value, 2) for value in vector]))

    unit_vec = []

    for value in vector:
        unit_vec.append(value/mag)

    return np.array(unit_vec)



def subtract(word1, word2, model):

    """
    Calculates vec(word1) - vec(word2)
    Input: word1 (str), word2 (str), model (word2vec model)
    Output: resulting vector
    """
    if (word1 in model.vocab) and (word2 in model.vocab):

        vec1 = model[word1]
        vec2 = model[word2]

        vec_result = np.subtract(vec1, vec2)
    else:
        vec_result = 'OOV'

    return vec_result


def sim_wv(wv1, wv2, model):

    """
    Calculate cosine similarity of words
    (represented either by a numpy vector or a string)
    Input: word1 (str or numpy array), word2 (str or numpy array), model (w2v model)
    (Unit vectors are calculated)
    Output: cosine similarity between vectors (float)
    """

    # Normalize vectors before calculating their dot product:

    if type(wv1) == str:
        if wv1 in model.vocab:
            vec1 = model[wv1]
        else:
            vec1 = 'OOV'
    else:
        vec1 = wv1

    if type(wv2) == str:
        if wv2 in model.vocab:
            vec2 = model[wv2]
        else:
            vec1 = 'OOV'
    else:
        vec2 = wv2

    # Only calculate sim if words in the model (i.e. not str 'OOV')
    if (type(vec1) != str) and (type(vec2) != str):
        vec1_unit = unit_vector(vec1)
        vec2_unit = unit_vector(vec2)
        sim_vec = np.dot(vec1_unit, vec2_unit)
    else:
        sim_vec = 0.0

    return sim_vec





def nearest_neighbors_subtracted(word1, word2, model):

    if (word1 in model.vocab) and (word2 in model.vocab):
        sub_vec = subtract(word1, word2, model)
        neighbors = model.similar_by_vector(sub_vec, topn = 10, restrict_vocab=None)
    else:
        neighbors = [('-', '-')]

    return neighbors


def highest_sim_word_list(word, word_list, model):

    sims = []

    if word in model.vocab:

        for w in word_list:

            if w in model.vocab:

                sim = sim_wv(word, w, model)
                sims.append((sim, w))
    if sims:
        return max(sims)
    else:
        return (0.0, '-')





if __name__ == '__main__':

    #replace this with the path to your the word2vec model:

    model_path = '../model/movies.bin'
    model = load_model(model_path)

    test_word1 = 'star'
    test_word2 = 'actor'

    test_vec1 = model['star']
    test_vec2 = model['actor']

    sim1 = sim_wv(test_word1, test_word2, model)
    sim2 = sim_wv(test_vec1, test_vec2, model)

    print('Does sim1 equal sim2 ?')
    print('sim1: ', sim1)
    print('sim2: ', sim2)

    # check if highest_sim_word_list works:

    word = 'actor'
    word_list = ['actress', 'star', 'director', 'red']

    highest_sim_word = highest_sim_word_list(word, word_list, model)
    print('highest sim with "actor": ', highest_sim_word)

    # test if model is loaded in the correct format:

    for n, word in enumerate(model.vocab):
        print(word)
        if n == 3:
            break
