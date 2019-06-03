from collections import defaultdict
import sys

def get_attributes(annotation):

    attr_dict = defaultdict(list)

    with open('attributes-validation.txt') as infile:
        lines = infile.read().strip().split('\n')

    for line in lines:
        line_list = line.split('\t')

        attr = line_list[0]

        an = '-'.join(sorted(line_list[1:]))

        #for an in line_list[1:]:
        attr_dict[an].append(attr)

    return attr_dict[annotation]


if __name__ == '__main__':

    annotation = sys.argv[1]

    print(get_attributes(annotation))
