import sys
from embeddings import load_model, sim_wv, highest_sim_word_list
from utils import load_triples, results_to_file, decisions_to_file
from wordnet import get_all_definitions, get_syn_depth, get_syns_depths
from wordnet import get_all_synsets


def sim_definition(prop, definition, model):

    # flat_list = [item for sublist in l for item in sublist]

    def_sim = highest_sim_word_list(prop, definition, model)

    return def_sim



def get_highest_def_sim(prop, definition_dict, model):

    sim_syn_list = []

    for syn, definition in definition_dict.items():

        max_sim = highest_sim_word_list(prop, definition, model)[0]

        sim_syn_list.append((max_sim, syn))


    return max(sim_syn_list)



def sim_def_check(concept1, concept2, prop, threshold1, threshold2):


    """
    Input: concept1 (str), concept2 (str), threshold1, threshold2 (float)
    Output: Dictionary recording decisions
    Checks whether the attribute is in any of the definitions of concept1 and
    concept2
    """

    decision_dict = dict()

    def_dict1 = get_all_definitions(concept1)
    def_dict2 = get_all_definitions(concept2)

    def1_answer = 0
    def2_answer = 0

    syns_concept1 = get_all_synsets(concept1)

    decision_dict['depths_concept1'] = ' '.join([str(d) for d in get_syns_depths(syns_concept1)])
    decision_dict['level'] = '-'
    decision_dict['decision_depth'] = '-'

    def_sim1, syn1 = get_highest_def_sim(prop, def_dict1, model)
    def_sim2, syn2 = get_highest_def_sim(prop, def_dict2, model)


    if (def_sim1 > threshold1) and (def_sim2 < threshold2):
        answer = '1'
        if syn1 in syns_concept1:
            decision_dict['level'] = 'synset'
        else:
            decision_dict['level'] = 'hypernym'
        decision_dict['decision_depth'] = get_syn_depth(syn1)


    elif (def_sim1 > threshold1) and (def_sim2 > threshold2):
        answer = '0'

    elif (def_sim1 < threshold1) and (def_sim2 > threshold2):
        answer = '0'

    else:
        answer = None

    decision_dict['answer'] = answer

    return decision_dict


def def_extended_system(data, threshold1, threshold2, model):


    triples = load_triples(data)
    answers = []
    decision_dicts = []
    name = 'def_extended_'+str(threshold1)+'-'+str(threshold2)+'_'+data


    for triple in triples:
        concept1 = triple[0]
        concept2 = triple[1]
        prop = triple[2]

        def_answer = None

        def_decision_dict = sim_def_check(concept1, concept2, prop, threshold1, threshold2)
        decision_dicts.append(def_decision_dict)
        def_answer = def_decision_dict['answer']

        if def_answer:
            answers.append(def_answer)
        else:
            answers.append('0')


    print('len data ', len(triples))
    print('len answers ', len(answers))
    results_to_file(triples, answers, name)
    decisions_to_file(triples, decision_dicts, name)



if __name__ == '__main__':

    data = sys.argv[1]

    # replace this with the path to your the word2vec model
    model_path = '../model/movies.bin'
    model = load_model(model_path)
    prop = 'shine'
    definition_dict = get_all_definitions('star')
    highest_sim_syn = get_highest_def_sim(prop, definition_dict, model)
    print(highest_sim_syn)

    threshold1 = 0.75
    threshold2 = 0.23

    def_extended_system(data, threshold1, threshold2, model)
