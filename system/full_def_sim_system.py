import sys
from embeddings import load_model, sim_wv, highest_sim_word_list
from utils import load_triples, results_to_file, decisions_to_file
from wordnet import get_all_definitions


def sim_definition(prop, definition_dict, model):

    definitions = [word for def_list in definition_dict.values() for word in def_list]
    # flat_list = [item for sublist in l for item in sublist]

    def_sim = highest_sim_word_list(prop, definitions, model)

    return def_sim
