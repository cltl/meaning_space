import sys
from embeddings import load_model, sim_wv
from utils import load_triples, results_to_file, decisions_to_file
from wordnet import get_all_definitions, get_syn_depth, get_syns_depths
from wordnet import get_all_synsets, check_if_syn_in_hyponyms
import os

def sim_definition(prop, definition, model):

    #flat_list = [item for sublist in l for item in sublist]
    #definition_list = definition_dict.values()
    #definitions = [w for definition in definition_list for w in definition]
    sims = []
    for word in definition:
        if (word in model.vocab) and (prop in model.vocab):
            sims.append((sim_wv(word, prop, model)))
        else:
            sims.append(0.0)
    if sims:
        return max(sims)
    else:
        return 0.0



def get_highest_def_sim(prop, definition_dict, model):

    sim_syn_list = []

    for syn, definition in definition_dict.items():

        max_sim = float(sim_definition(prop, definition, model))

        sim_syn_list.append((max_sim, syn))

    return max(sim_syn_list)




def sim_def_check(concept1, concept2, prop, threshold1, threshold2, model):


    """
    Input: concept1 (str), concept2 (str), threshold1, threshold2 (float)
    Output: Dictionary recording decisions
    Checks whether the attribute is in any of the definitions of concept1 and
    concept2
    """

    decision_dict = dict()

    def_dict1 = get_all_definitions(concept1)
    def_dict2 = get_all_definitions(concept2)



    decision_dict['system'] = 'def_sim'


    def_sim1, syn1 = get_highest_def_sim(prop, def_dict1, model)
    def_sim2, syn2 = get_highest_def_sim(prop, def_dict2, model)


    if (def_sim1 > threshold1) and (def_sim2 < threshold2):
        answer = '1'



    elif (def_sim1 > threshold1) and (def_sim2 > threshold2):
        answer = '0'


    elif (def_sim1 < threshold2) and (def_sim2 > threshold1):
        answer = '0'

    elif (def_sim1 < threshold2) and (def_sim2 < threshold2):
        answer = '0'


    else:
        answer = None

    decision_dict['answer'] = answer



    return decision_dict


def def_extended_system(data, threshold1, threshold2, model):


    triples = load_triples(data)
    answers = []
    decision_dicts = []
    name = 'def_extended_'+data

    total = len(triples)
    for n, triple in enumerate(triples):
        concept1 = triple[0]
        concept2 = triple[1]
        prop = triple[2]

        def_decision_dict = sim_def_check(concept1, concept2, prop, threshold1, threshold2, model)
        decision_dicts.append(def_decision_dict)
        def_answer = def_decision_dict['answer']

        if def_answer:
            answers.append(def_answer)
        else:
            answers.append('0')

        if n in range(0, total, 50):
            status = n/total
            print(status, ' of the test data classified ')


    print('len data ', len(triples))
    print('len answers ', len(answers))
    results_to_file(triples, answers, name)
    decisions_to_file(triples, decision_dicts, name)



if __name__ == '__main__':


    data = sys.argv[1]

    if not os.path.isdir('../results'):
        os.mkdir('../results')

    # replace this with the path to your the word2vec model
    #model_path = '../model/movies.bin'
    model_path = '../../../Data/word2vec/GoogleNews-vectors-negative300.bin'
    model = load_model(model_path)
    #prop = 'shine'
    #definition_dict = get_all_definitions('star')
    #highest_sim_syn = get_highest_def_sim(prop, definition_dict, model)
    #print(highest_sim_syn)

    threshold1 = 0.75
    threshold2 = 0.23

    def_extended_system(data, threshold1, threshold2, model)
