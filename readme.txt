System submitted to SemEval 2018 Task 10: Capturing discriminative attributes

Requirements:

Python 3
Gensim 
Numpy
NLTK
Pandas 

Data:

SemEval evaluation scripts (to be downloaded from https://github.com/dpaperno/DiscriminAtt/) (I suggest to store them in data/)

A distributional semantic model (we used the GoogleNews skiagram model downloaded from https://drive.google.com/file/d/0B7XkCwpI5KDYNlNUTTlSS21pQmM/edit). I included code to create a small toy model with NLTK (in model/create_toy_model.py). 

Scripts to run the different systems can be found in systems/:

- similarity system: systems/baseline_embedding_sim.py
- subtraction system: systems/baseline_embedding_subtraction.py
- definition system: systems/baseline_wordnet.py

- full system similarity: system/full_def_embedding_sim_system.py (best performance, ranked 5th out of 9 systems in the final ranking)
- full system subtraction: system/full_def_subtraction_system.py

- definitions extended with embeddings: system/definitions.extended.py

The annotations we used for our analysis in the system description paper can be found in attribute_annotation/. The annotations are used in our analysis of system performances across different attribute categories included in our task paper. The graphs can be found in evaluation/graphs_plotly. 

[references to system description and task paper will be added]. 



