import csv, glob, re
from .mention import Mention
from .featureUtils import *
import json

cluster_number = 0
featureUtils = FeatureUtils()


def read_all_files(path="./data/example/*.tsv"):
    featureUtils.init_stanza()
    all_mentions = []
    all_clusters = []
    all_filenames = []
    for file in glob.glob(path):
        mentions, clusters = read_one_files(file)
        all_mentions.append(mentions)
        all_clusters.append(clusters)
        all_filenames.append(file)
    return all_mentions, all_clusters, all_filenames

def read_one_files(file):
    global cluster_number
    cluster_number = 0
    mentions = {}
    clusters_dict = {}
    with open(file, encoding="utf8") as tsvfile:
        tsv_reader = csv.reader(tsvfile, delimiter="\t", quoting=csv.QUOTE_NONE)
        for line in tsv_reader:
            if len(line) == 0 or line[0][0] == "#" or line[3] == "_":
                continue
            ids = parse_mention_ids(line[0], line[3])
            word = line[2]
            sentence = line[0].split("-")[0]
            position = line[0].split("-")[1]
            add_mentions(ids, mentions, word, sentence, position, clusters_dict)
            if line[6] != "_":
                parse_clusters(line[0], line[5], line[6], clusters_dict)
    mentions, clusters = update_mention_ids(mentions, clusters_dict)
    return mentions, clusters


def parse_mention_ids(file_sentence_pos, file_mentions):
    """Gets the id of a mention, either the id given in the file (e.g. person[1] => id = 1)
    or if this does not exist, the first part of the line ("sentence-index") is chosen as id."""
    ids = []
    for id_type in file_mentions.split("|"):
        id = re.search("\d+", id_type)
        ids.append(id.group(0) if id else file_sentence_pos)
    return ids

def add_mentions(ids, mentions, word, sentence, position, clusters_dict):
    """Creates a mention and adds it to mentions-array. The cluster for the mention is
    also initialized if it does not exist."""
    global cluster_number
    for id in ids:
        if id not in mentions:
            mention = Mention(id, word, sentence, position)
            mentions[id] = mention
            # Initialize cluster
            if id not in clusters_dict:
                clusters_dict[id] = cluster_number
                cluster_number += 1
            
        else:
            mentions[id].append_word(word)
            # The last time this is updated will be for the last word
            mentions[id].set_end_position(position) 

def parse_clusters(file_sentence_pos, file_cluster_type, file_cluster_relations, clusters_dict):
    """Parses file (last part of lines) for info about clusters."""
    global cluster_number
    cluster_relations = file_cluster_relations.split("|")
    cluster_type = file_cluster_type.split("|")
    for i in range(len(cluster_relations)):
        relation = cluster_relations[i]
        relation_type = cluster_type[i]
        if relation_type.find("bridge") == -1:        
            r = re.search("\d+_\d+", relation)
            if r:
                r = r.group(0).split("_")
                id1 = r[1] if r[1] != "0" else file_sentence_pos
                id2 = r[0] if r[0] != "0" else re.search("\d+-\d+", relation).group(0)
            else:
                id1 = file_sentence_pos
                id2 = re.search("\d+-\d+", relation).group(0)

            if id1 not in clusters_dict:
                clusters_dict[id1] = cluster_number
                cluster_number += 1
            clusters_dict[id2] = clusters_dict[id1]

def update_mention_ids(mentions_dict, clusters_dict):
    """Updates mention ids in mentions and clusters to 1, 2, 3..."""
    
    id = 0
    clusters = []
    mentions = []
    for m in mentions_dict:
        oldId = mentions_dict[m].id
        mentions_dict[m].update_id(id)
        mentions.append(mentions_dict[m])
        clusters.append(clusters_dict[oldId])
        id+=1
        mentions_dict[m].calculate_headword(featureUtils)
    return mentions, clusters


if __name__ == "__main__":
    all_files_mentions, all_files_clusters = read_all_files("./data/example/*.tsv")

    for i in range(len(all_files_mentions)):
        print("\n\nFile " + str(i+1) + ":")
        mentions = all_files_mentions[i]
        clusters = all_files_clusters[i]
        for id in range(len(mentions)):
            print(mentions[id])
        print("\nClusters:")
        print(clusters)
