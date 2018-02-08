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

def sim(word1, word2, model):

    """
    Calculate cosine similarity between word1 and word2
    Check if words are in the model vocabulary, if not,
    return a cosine similarity of 0.0
    Input: word1 (str), word2 (str), model (Word2Vec model)
    Output: cosine similarity (float)
    """

    if (word1 in model.vocab) and (word2 in model.vocab):
        sim = model.similarity(word1, word2)

    else:
        sim = 0.0

    return sim


def embedding_sim(concept1, concept2, prop, model):


    if (concept1 in model.vocab) and (prop in model.vocab):
        sim_concept1=model.similarity(concept1, prop)
    else:
        sim_concept1=0

    if (concept2 in model.vocab) and (prop in model.vocab):
        sim_concept2=model.similarity(concept2, prop)
    else:
        sim_concept2=0

    return sim_concept1, sim_concept2

def neighbor_rank(concept1, concept2, prop, model):

    if (concept1 in model.vocab) and (prop in model.vocab):
        rank1 = model.rank(concept1, prop)
    else:
        rank1 = 0
    if (concept2 in model.vocab) and (prop in model.vocab):
        rank2 = model.rank(concept2, prop)
    else:
        rank2 = 0

    return rank1, rank2


def unit_vector(vector):

    mag = math.sqrt(sum([pow(value, 2) for value in vector]))

    unit_vec = []

    for value in vector:
        unit_vec.append(value/mag)

    return np.array(unit_vec)

def get_offset(word_pos, word_neg, model):

    word_pos_vec = model[word_pos]
    word_neg_vec = model[word_neg]

    mean_list = []

    mean_list.append(word_pos_vec * 1.0)
    mean_list.append(word_neg_vec * -1.0)

    mean = unit_vector(np.array(mean_list).mean(axis = 0)).astype(REAL)

    return mean

def subtract(word1, word2, model):

    vec1 = model[word1]
    vec2 = model[word2]

    c = unit_vector(np.subtract(vec1, vec2))

    return c


def subtract_add(word1, word2, word3, model):

    vec1 = model[word1]
    vec2 = model[word2]
    vec3 = model[word3]

    d = unit_vector(np.add(np.subtract(vec2, vec1), vec3))

    return d

def sim_subtraction(word1, word2, word3, model):

    if (word1 in model.vocab) and (word2 in model.vocab) and (word3 in model.vocab):

        sub_vec = subtract(word1, word2, model)
        word3_vec = unit_vector(model[word3])

        sim_sub = np.dot(sub_vec, word3_vec)
    else:
        sim_sub = 0.0

    return sim_sub

def analogy_prop_sim(word1, word2, word3, model):

    if (word1 in model.vocab) and (word2 in model.vocab) and (word3 in model.vocab):

        vec_d = subtract_add(word1, word2, word3, model)
        vec3 = model[word3]

        sim_prop_d = np.dot(vec_d, vec3)
    else:
        sim_prop_d = 0.0

    return sim_prop_d


def nearest_neighbors_subtracted(word1, word2, model):

    if (word1 in model.vocab) and (word2 in model.vocab):
        sub_vec = subtract(word1, word2, model)
        neighbors = model.similar_by_vector(sub_vec, topn = 10, restrict_vocab=None)
    else:
        neighbors = [('-', '-')]

    return neighbors

def get_closest_of_list(word, word_list, model):

    most_similar_word = model.most_similar_to_given(word, word_list)

    return most_similar_word



def analogy(concept1, concept2, prop, model):

    # Example: king:queen = man:X
    # X=queen-king+man
    # Data: optician:eyes = orthodontist:X
    # X=eyes-optician+orthodontist
    #General: concept2-concept1+prop
    closest_word=model.most_similar(positive=[concept2,prop], negative=[concept1], topn=1)

    return closest_word[0]

def analogy_property(concept1, concept2, prop, model):

    # Example: king:queen = man:X
    # X=queen-king+man
    # Data: optician:eyes = orthodontist:X
    # X=eyes-optician+orthodontist
    #General: concept2-concept1+prop
    closest_word=model.most_similar(positive=[concept2,prop], negative=[concept1], topn=1)[0]

    sim_prop_closest = model.similarity(closest_word[0], prop)

    return sim_prop_closest

def analogy_input_ignore(concept1, concept2, prop, model):

    # Example: king:queen = man:X
    # X=queen-king+man
    # Data: optician:eyes = orthodontist:X
    # X=eyes-optician+orthodontist
    #General: concept2-concept1+prop
    closest_word=model.most_similar(positive=[concept2,prop], negative=[concept1], topn=1, input_ignore=False)

    return closest_word[0]


if __name__ == '__main__':

    #replace this with the path to your the word2vec model:

    model_path = '../model/movies.bin'
    model = load_model(model_path)

    # test if model is loaded in the correct format:

    for n, word in enumerate(model.vocab):
        print(word)
        if n == 10:
            break
