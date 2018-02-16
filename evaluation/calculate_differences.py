import glob
from collections import defaultdict
import pandas as pd



def get_cat_performances(list_systems, cutoff):

    sys_dict = dict()



    for system_name in list_systems:

        system_name = system_name.replace('-', '_')
        print(system_name)
        system = 'categories/cat_'+system_name+'.txt'

        cat_dict = dict()

        with open(system) as infile:
            for line in infile.read().strip().split('\n')[1:]:

                category = line.split(',')[0]
                system_data = []

                n = int(line.split(',')[5])


                if n > cutoff:
                    f1_average = float(line.split(',')[9])
                    cat_dict[category] = f1_average



            sys_dict[system[15:].split('.')[0]] = cat_dict



    return sys_dict


def get_most_frequent_categories(list_systems, n):


    system_name = list_systems[0]
    system_name = system_name.replace('-', '_')
    print(system_name)
    system = 'categories/cat_'+system_name+'.txt'
    cat_freqs = []

    with open(system) as infile:
        for line in infile.read().strip().split('\n')[1:]:

            category = line.split(',')[0]
            freq = int(line.split(',')[5])

            cat_freqs.append((freq, category))


    return [cat for freq, cat in sorted(cat_freqs, reverse = True)[:n]]




def compare_performances(list_systems, cutoff):

    sys_dict = get_cat_performances(list_systems, cutoff)



    df = pd.DataFrame.from_dict(sys_dict)

    df_t = df.T

    score_differences = []
    for n, c in enumerate(df_t):
        #scores = [v for v in df_t[c]]
        print(c)

        value1 = df_t[c][0]
        value2 = df_t[c][1]

        diff = abs(value1 - value2)
        score_differences.append((diff, c))


    target_categories = [diff[1] for diff in sorted(score_differences, reverse = True,)[:9]]


    return target_categories




if __name__ == '__main__':
    cutoff = 1
    list_systems = ['def_baseline_toy', 'embedding_sim_baseline_toy', ]
    #compare_performances(list_systems, cutoff)
    cats = get_most_frequent_categories(list_systems, 5)

    print(cats)



    #for i, s in df.iterrows():
    #    print(s)

    #for system, performances in sys_dict.items():
    #    print(system, len(performances))
