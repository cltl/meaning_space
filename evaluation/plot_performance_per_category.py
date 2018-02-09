import glob
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import os
from calculate_differences import compare_performances
# Systems: in files starting with 'error_analysis_'
# Performance per category: in 'error_analysis_system.csv' file:
    # column1: category
    # column2: tp
    # column2: tn
    # column3: fp
    # column4: fn
    # column5: sum of all cases in the category
    # column6: precision
    # column7: recall
    # column 8: f1 f1_positive
    # column 9: f1 average



def get_performance(list_systems, list_categories):

    sys_dict = defaultdict(list)

    systems = []

    for system_name in list_systems:

        system = 'error_analysis_'+system_name+'.csv'

        #names.append(system.lstrip('error_analysis').rstrip('.csv'))
        with open(system) as infile:
            for line in infile.read().strip().split('\n')[1:]:
                category = line.split(',')[0]
                if category in list_categories:
                    print(category)
                    system_data = []
                    n = int(line.split(',')[4])
                    f1_average = float(line.split(',')[8])
                    system_data.append(system[15:].split('.')[0])
                    system_data.append(category)
                    system_data.append(f1_average)
                    #sys_dict['systems'].append(category+'_'+system)
                    #sys_dict['performance'].append(f1_average)

                    systems.append(system_data)

    return systems #, all_categories #, names



def plot_performances(list_systems, list_categories, name):

    if not os.path.isdir('graphs'):
        os.mkdir('graphs')

    dpoints  = get_performance(list_systems, list_categories)
    print(dpoints)

    df = pd.DataFrame(dpoints, columns = ['system', 'category', 'performance']) #.set_index('system')
    print(df)

    sns.set_style('whitegrid')
    ax = sns.barplot(x = 'system', y = 'performance', hue = 'category', data = df)
    ax.legend(loc=2)
    plt.savefig('graphs/'+name+'.png')
    plt.show()




if __name__ == '__main__':

    #list_systems = glob.glob('error_analysis*.csv')[:3]

    list_systems = ['embeddings_baseline', 'analogy-scaled_mlp_emb_rev1-1-logistic']
    #list_systems = ['embeddings_baseline', 'analogy-scaled_mlp_emb_rev1-1-logistic']
    # Wordnet constraint systems in isolation:
    #list_systems = [f.lstrip('error_analysis_').split('.')[0] for f in glob.glob('*wn_constraints_*.csv') if '-rev' in f]
    #list_categories = ['animate-bodypart_organ-object-part', 'material', 'appearance-color', 'event', 'animate-gender-object-person', 'magnitude-size', 'appearance-duration-magnitude-shape']
    cutoff = 10
    list_categories = compare_performances(list_systems, cutoff)
    name = 'sim_subtraction_baselines'+str(cutoff)
    #name = 'embedding_baselines_manual_cat-list'
    plot_performances(list_systems, list_categories, name)
