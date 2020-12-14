from .readFiles import read_all_files
from .constructGraphs import construct_all_graphs
import json

def generate_training_data(path="./data/example/*.tsv"):
    mentions, clusters, _ = read_all_files(path)
    graphs = construct_all_graphs(mentions)
    
    return list(zip(graphs, clusters))

def generate_test_data(path="./data/example/*.tsv"):
    mentions, clusters, all_files = read_all_files(path)
    graphs = construct_all_graphs(mentions)
    
    id_to_mention_list = []
    for mentionlist in mentions:
        id_to_mention = {}
        for mention in mentionlist:
            id_to_mention[mention.id] = mention
        id_to_mention_list.append(id_to_mention)
    return list(zip(graphs, clusters, id_to_mention_list, all_files))

if __name__ == "__main__":
    graphs, clusters = generate_data()
    print(graphs)
    print(clusters)