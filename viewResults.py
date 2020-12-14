import json
import csv
import argparse

#  https://stackoverflow.com/questions/287871/how-to-print-colored-text-in-python
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

parser = argparse.ArgumentParser(description='Shows clusters in the selected text.')
parser.add_argument('filename', default='GUM_voyage_tulsa', nargs='?',
                    help='name of the file you want to analyse, without extension. Must be in testing dir.')
parser.add_argument('--actual', action='store_true',
                    help='show actual clusters (default: show predicted)')

args = parser.parse_args()


name = args.filename
with open(str('actualClusters/' + name + '.json'), 'r', encoding='utf-8') as f:
        actual = json.load(f)

with open(str('predictedClusters/' + name + '.json'), 'r', encoding='utf-8') as f:
        predicted = json.load(f)

with open(str('mappings/' + name + '.json'), 'r', encoding='utf-8') as f:
        mapping = json.load(f)


text = []
with open('data/GUM_tsv/testing/' + name + '.tsv', encoding="utf8") as tsvfile:
        tsv_reader = csv.reader(tsvfile, delimiter="\t", quoting=csv.QUOTE_NONE)
        for line in tsv_reader:
            if len(line) == 0 or line[0][0] == "#":
                continue
            word = line[2]
            sentence = line[0].split("-")[0]
            position = line[0].split("-")[1]
            text.append((word, int(sentence), int(position)))

if args.actual: 
        clusters = actual['clusters']
        viewType = 'actual'
else:
        clusters = predicted['clusters']
        viewType = 'predicted'

print('You are viewing {} clusters for file {}'.format(viewType, name))
print('Press enter to see a new cluster, or q to quit')
command = input()
if command == 'q':
        exit()
for cluster_id in clusters:
        cluster = clusters[cluster_id]
        if len(cluster) == 1:
                continue
        is_in_cluster = set()
        min_sentence = 10000000
        max_sentence = 0
        for mention in cluster:
                (sentence, start_pos, end_pos) = mapping[str(mention)]
                sentence = int(sentence)
                start_pos = int(start_pos)
                end_pos = int(end_pos)
                min_sentence = min(sentence, min_sentence)
                max_sentence = max(sentence, max_sentence)
                for pos in range (start_pos, end_pos+1):
                        is_in_cluster.add((sentence, pos))

        for item in text:
                (word, sentence, position) = item
                if sentence < min_sentence-1:
                        continue
                if sentence > max_sentence+1:
                        continue
                if word != '.' and word != ',':
                        print(" ", end="")
                if (sentence, position) in is_in_cluster:
                        print( bcolors.WARNING + word + bcolors.ENDC, end="")
                else:
                        print(word, end="")
        print()
        print()
        print()
        command = input()
        if command == 'q':
                break
