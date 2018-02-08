import sys
from embeddings import load_model, sim_wv, highest_sim_word_list
from utils import load_triples, results_to_file, decisions_to_file
from wordnet import get_all_definitions
