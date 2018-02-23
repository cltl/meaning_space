import glob
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import os
from calculate_differences import compare_performances, get_most_frequent_categories
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
        system_name = system_name.replace('-', '_')
        print(system_name)

        system = 'categories/cat_'+system_name+'.txt'

        #names.append(system.lstrip('error_analysis').rstrip('.csv'))
        with open(system) as infile:

            system = system[15:]

            if system.startswith('baseline_'):
                system = system.split('_', 1)[1]
            system_name = '-'.join(system.split('.')[0].split('_')[:-1])




            for line in infile.read().strip().split('\n')[1:]:
                category = line.split(',')[0]
                if category in list_categories:

                    system_data = []
                    n = int(line.split(',')[4])
                    f1_average = float(line.split(',')[8])
                    system_data.append(system_name)
                    system_data.append(category)
                    system_data.append(f1_average)
                    #sys_dict['systems'].append(category+'_'+system)
                    #sys_dict['performance'].append(f1_average)

                    systems.append(system_data)

    return systems #, all_categories #, names



def plot_performances(list_systems, list_categories, name):

    if not os.path.isdir('category_graphs'):
        os.mkdir('category_graphs')

    dpoints  = get_performance(list_systems, list_categories)


    df = pd.DataFrame(dpoints, columns = ['system', 'category', 'performance']) #.set_index('system')

    df.to_csv('category_graphs/'+name+'.csv')

    sns.set_style('whitegrid')
    #n_colors = len(list_categories)
    my_p = sns.color_palette("cubehelix", 10)

    #ax = sns.barplot(x = 'system', y = 'performance', hue = 'category', data = df, palette = my_p)

    ax = sns.factorplot(x = "category", y= "performance",  col = 'system',
                    data = df, kind="bar", ci = None, aspect = .6, hline = 0,
                    palette=my_p, size = 9) #, legend_out=False, size=6)
    (ax.set_axis_labels("", "Performance")
    .set_xticklabels(df['category'], rotation = 90)
    .set_titles('{col_name} {col_var}')
    .set(ylim = (0, 1))
    .despine(left = True))


    #plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    #ax.legend(loc=2)
    #ax.despine(left=True)
    #ax.set_axis_labels('category', 'performance')
    plt.savefig('category_graphs/'+name+'.png')
    plt.show()




if __name__ == '__main__':

    #list_systems = glob.glob('error_analysis*.csv')[:3]

    #list_systems = ['baseline_sim_validation', 'baseline_subtraction_validation', ]
    #list_systems = ['baseline_sim_validation', 'baseline-definitions-validation', ]
    #list_systems = ['baseline-subtraction-validation', 'baseline-definitions-validation', ]
    #list_systems = ['baseline_sim_validation', 'baseline-subtraction-validation', 'baseline-definitions-validation' ]
    #list_systems = ['embeddings_baseline', 'analogy-scaled_mlp_emb_rev1-1-logistic']
    # Wordnet constraint systems in isolation:
    #list_systems = [f.lstrip('error_analysis_').split('.')[0] for f in glob.glob('*wn_constraints_*.csv') if '-rev' in f]
    #list_categories = ['animate-bodypart_organ-object-part', 'material', 'appearance-color', 'event', 'animate-gender-object-person', 'magnitude-size', 'appearance-duration-magnitude-shape']
    cutoff = 10
    n = 10
    list_categories_diff = compare_performances(list_systems, cutoff)
    #list_categories_most_freq = get_most_frequent_categories(list_systems, n)

    name = '-vs-'.join(list_systems)+'-'+str(cutoff)

    plot_performances(list_systems, list_categories_diff, name+'-diff')
    #plot_performances(list_systems, list_categories_most_freq, name+'-freq')
