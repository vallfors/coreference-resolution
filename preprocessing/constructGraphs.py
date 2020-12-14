import numpy as np
from .readFiles import read_all_files
from .sieves import ( sieve_one, 
                        sieve_two, 
                        sieve_three, 
                        sieve_four, 
                        sieve_five, 
                        sieve_six )
from .features import ( string_matching_headword, 
                        pronouns_and_string_match, 
                        edit_distance_headword, 
                        proper_names_and_string_match, 
                        both_proper_names_or_pronouns, 
                        compatible_pronouns,
                        same_named_entity,
                        distance_sentences, 
                        distance_mentions,
                        pronoun_1,
                        pronoun_2,
                        definite_2,
                        number,
                        gender,
                        demonstrative_2,
                        both_proper_nouns,
                        animacy,
                        basic_features)

def construct_all_graphs(all_files_mentions):
    graphs = []
    for i in range(len(all_files_mentions)):
        mentions = all_files_mentions[i]
        graph = construct_graph(mentions)
        graphs.append(graph)
    return graphs

def construct_graph(mentions):
    graph = []
    number_of_mentions = len(mentions)
    number_of_sentences = mentions[number_of_mentions-1].sentence
    for i in range(number_of_mentions):
        neighbours = []
        for j in range(i+1, number_of_mentions):
            if sieve_one(mentions[i], mentions[j]) or sieve_two(mentions[i], mentions[j]) or sieve_three(mentions[i], mentions[j]) or sieve_four(mentions[i], mentions[j]) or sieve_five(mentions[i], mentions[j]) or sieve_six(mentions[i], mentions[j]):
                features = add_features(mentions[i], mentions[j], number_of_mentions, number_of_sentences)
                neighbours.append((mentions[j].id, features))
        graph.append(neighbours)
    return graph


def add_features(m_i, m_j, number_of_mentions, number_of_sentences):
    featureResults = []
    for f in basic_features:
        featureResults.append(f(m_i, m_j))
    return np.array(featureResults)

if __name__ == "__main__":
    all_files_mentions, _ = read_all_files("./data/example/*.tsv")
    graphs = construct_all_graphs(all_files_mentions)
    for graph in graphs:
        print(graph)