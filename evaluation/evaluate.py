import glob
import sys

def load_data(data_file):
    # load gold data or system output
    with open(data_file) as infile:

        answers = [line.split(',')[3] for line in infile.read().strip().split('\n')]
        #triples = [(line.split(',')[0]) for line in infile.read().strip().split('\n')]

    return answers

def load_triples(data_file):
    # load gold data or system output
    with open(data_file) as infile:

        triples = [line.split(',')[:3] for line in infile.read().strip().split('\n')]
        #triples = [(line.split(',')[0]) for line in infile.read().strip().split('\n')]

    return triples

def f1_score(system_answers, gold_answers, system_triples, gold_triples):

    f1_positives = 0
    f1_negatives = 0

    tp = 0
    tn = 0
    fp = 0
    fn = 0
    result_dict = dict()

    # To make sure I always evaluate against the correct triple:

    # sanity check1:
    print(len(system_answers), len(gold_answers))

    #len(system_answers) == len(gold_answers), 'Lenght of answer lists differ'

    # sanity check2 - make sure the triples are identical



    if system_triples == gold_triples:


        for system_answer, gold_answer in zip(system_answers, gold_answers):

                if system_answer == '1' and gold_answer == '1':
                    tp = tp+1
                elif system_answer == '0' and gold_answer == '0':
                    tn = tn+1
                elif system_answer == '1' and gold_answer == '0':
                    fp = fp+1
                elif system_answer == '0' and gold_answer == '1':
                    fn = fn+1
        if tp>0:
            precision=float(tp)/(tp+fp)
            recall=float(tp)/(tp+fn)
            f1_positives = 2*((precision*recall)/(precision+recall))

            result_dict['Precision'] =  precision
            result_dict['Recall'] = recall
        else:
            result_dict['Precision'] = '-'
            result_dict['Recall'] = '-'


        if tn>0:
            precision=float(tn)/(tn+fn)
            recall=float(tn)/(tn+fp)
            f1_negatives = 2*((precision*recall)/(precision+recall))
        if f1_positives and f1_negatives:
            f1_average = (f1_positives+f1_negatives)/2.0
            result_dict['F1-average'] =  f1_average
        else:
            result_dict['F1-average'] = '-'
            #return f1_average

        #else:
            #return 0
        return result_dict
    else:
        return None

def evaluate(data):

    gold_answers = load_data('../data/'+data+'.txt')

    with open('results-summary-'+data+'.txt', 'w') as outfile:

        for results_file in glob.glob('../results/*'+data+'.txt'):

            print(results_file)
            system_answers = load_data(results_file)


            system_name = results_file.split('/')[-1].rstrip('.txt')

            results = f1_score(system_answers, gold_answers)

            if results != None:

                for res, val in results.items():
                    print(res, val)

                outfile.write(system_name+','+str(results['Precision'])+','+str(results['Recall'])+','+str(results['F1-average'])+'\n')

def evaluate_sort(data):

    gold_answers = load_data('../data/'+data+'.txt')
    gold_triples = load_triples('../data/'+data+'.txt')

    results_list = []


    for results_file in glob.glob('../results/*'+data+'.txt'):

        print(results_file)
        system_answers = load_data(results_file)
        system_triples = load_triples(results_file)


        system_name = results_file.split('/')[-1].rstrip('.txt').replace('_', '-')

        results = f1_score(system_answers, gold_answers, system_triples, gold_triples)

        if results != None:

            f1 = results['F1-average']

            if f1 == '-':
                f1 = 0.0

            results_list.append((f1, [system_name, str(results['Precision']), str(results['Recall']), str(results['F1-average'])]))
        else:
            results_list.append((0.0, [system_name, '-', '-', '-']))

    return sorted(results_list, reverse = True)



def results_to_file(results_list):

    with open('results-summary-'+data+'.txt', 'w') as outfile:

        for results in results_list:

            line_list = results[1]

            line_str = ','.join(line_list)

            outfile.write(line_str+'\n')



def results_to_table(results_list):



    print('\\begin{center}')
    print('\\begin{table}')
    print('\\begin{tabular}{| l | l | l | l |}')
    print('\\hline')
    print('System & Precision & Recall & F1-average \\\ \hline')
    print('\\hline')
    print(' &  &  & \\\ \hline')

    for results in sorted(results_list, reverse = True):
        line_list = results[1]


        line_list_rounded = []

        for n, r in enumerate(line_list):
            if n != 0:
                line_list_rounded.append(str(round(float(r), 2)))
            else:
                line_list_rounded.append(r)



        line_str = '&'.join(line_list_rounded)
        print(line_str+'\\\ \hline')


    print('\\end{tabular}')
    print('\\caption{Performance overview.}')
    print('\\end{table}')
    print('\\end{center}')




if __name__ == '__main__':

    data = sys.argv[1]
    results_list = evaluate_sort(data)
    results_to_file(results_list)
    results_to_table(results_list)
