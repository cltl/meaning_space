# create a toy w2v model
# based on https://streamhacker.com/2014/12/29/word2vec-nltk/

from gensim import models
from gensim.models import Word2Vec
from nltk.corpus import movie_reviews


mr = Word2Vec(movie_reviews.sents())

mr.wv.save_word2vec_format('movies.bin')


#model.wv.save_word2vec_format('model.bin')
#models.KeyedVectors.load_word2vec_format(filepath, binary=True)
