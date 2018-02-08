from nltk.corpus import wordnet as wn
from nltk import word_tokenize
from collections import defaultdict
from nltk.corpus import stopwords
#from nltk.stem.wordnet import WordNetLemmatizer


def get_all_synsets(word):

    """
    Input: word (str)
    Output: all wordnet synsets containing the word
    """

    syns = wn.synsets(word)

    return syns

def get_hypernyms(syn):

    """
    Input: a WordNet synset
    Output: all hypernyms of this synsets in the WordNet hierarchy
    """

    hypernyms = []

    for hyp in syn.hypernyms():
        if hyp not in hypernyms:
            hypernyms.append(hyp)
            for hyp2 in hypernyms:
                for hyp3 in hyp2.hypernyms():
                    if hyp3 not in hypernyms:
                        hypernyms.append(hyp3)
    return hypernyms



def get_all_hypernyms(word):

    """
    Input: word (str)
    Output: all synsets containing the word and all of their hypernym synsets
    """

    all_syns_hypernyms = []

    for syn in get_all_synsets(word):
        all_syns_hypernyms.append(syn)
        for hyp in get_hypernyms(syn):
            if hyp not in all_syns_hypernyms:
                all_syns_hypernyms.append(hyp)

    return all_syns_hypernyms



def get_all_definitions(word):

    """
    Input: word (str)
    Output: all definitions of the word senses and their hypernyms in WordNet
    """

    all_definitions = dict()

    all_syns_hypernyms = get_all_hypernyms(word)


    for syn in all_syns_hypernyms:

        definition = syn.definition()
        def_tokenized = word_tokenize(definition)

        all_definitions[syn] = [word for word in def_tokenized if word not in stopwords.words('english')]
        # Exclude stopwords

    return all_definitions


def get_syns_depths(syns):

    """
    Input: list of synsets
    Output: list of maximal depths of the synsets in the WordNet hierarchy"""

    syn_depths = [syn.max_depth() for syn in syns]

    return syn_depths

def get_syn_depth(syn):

    depth = syn.max_depth()

    return depth


def get_parts(synset):

    """
    Input: WordNet synset
    Output: All lemmas connected to the synsets via a meronymy relation
    """

    parts = []

    for mer in synset.part_meronyms():
        parts.append(mer)
    for mer in synset.substance_meronyms():
        parts.append(mer)
    for mer in synset.member_meronyms():
        parts.append(mer)
    return parts



def get_all_parts(word):

    """
    Input: word (str)
    Output: all lemma connected to the any of the synsets or their hypernyms
    or their parts via a meronymy relation"""

    all_parts = set()

    all_syns_hypernyms = get_all_hypernyms(word)

    all_syns = set()

    for syn in all_syns_hypernyms:

        for part in get_parts(syn):
            for lemma in part.lemmas():
                all_parts.add(str(lemma.name()))
            for subpart in get_parts(part):
                for lemma in subpart.lemmas():
                    all_parts.add(str(lemma.name()))

    return all_parts

def get_lemmas(syn):

    lemmas = [str(lemma.name()) for lemma in syn.lemmas()]

    return lemmas
