from scorch import main
import json

def save_scores_to_file(name, actual, predicted):
    """ Saves the actual scores and the predicted scores as json files 
    so that scorch can evaluate them. """
    #print("Actual: ")
    #print(actual)
    #print(len(actual))
    #print("Predicted: ")
    #print(predicted)
    #print(len(predicted))

    translate_actual = {}
    translate_predicted = {}
    translate_index = 0
    actual_clusters = {}
    predicted_clusters = {}
    for mention in range(len(actual)):
        actual_cluster = actual[mention]
        predicted_cluster = predicted[mention]

        if actual_cluster not in translate_actual:
            translate_actual[actual_cluster] = translate_index
        if predicted_cluster not in translate_predicted:
            translate_predicted[predicted_cluster] = translate_index

        cluster = translate_actual[actual_cluster]
        if cluster in actual_clusters:
            actual_clusters[cluster].append(mention)
        else:
            actual_clusters[cluster] = [mention]

        cluster = translate_predicted[predicted_cluster]
        if cluster in predicted_clusters:
            predicted_clusters[cluster].append(mention)
        else:
            predicted_clusters[cluster] = [mention]
        
        translate_index += 1

    actual_json = {"name": name, "type": "clusters", "clusters": actual_clusters}
    predicted_json = {"name": name, "type": "clusters", "clusters": predicted_clusters}
    
    """
    predicted_clusters = {}
    for mention in range(len(predicted)):
        cluster = predicted[mention]
        if cluster in predicted_clusters:
            predicted_clusters[cluster].append(mention)
        else:
            predicted_clusters[cluster] = [mention]
    predicted_json = {"name": name, "type": "clusters", "clusters": predicted_clusters}
    """

    with open(str('actualClusters/' + name + '.json'), 'w', encoding='utf-8') as f:
        json.dump(actual_json, f, ensure_ascii=False, indent=4)
    with open(str('predictedClusters/' + name + '.json'), 'w', encoding='utf-8') as f:
        json.dump(predicted_json, f, ensure_ascii=False, indent=4)

# Saves a mapping from mention id to sentence and start/end positions in the text.
def save_mapping_to_file(name, mapping):
    mapping_json = {}
    for key in mapping:
        mapping_json[key] = (mapping[key].sentence, mapping[key].start_position, mapping[key].end_position)
    with open(str('mappings/' + name + '.json'), 'w', encoding='utf-8') as f:
        json.dump(mapping_json, f, ensure_ascii=False, indent=4)

def print_scores():
    """ Prints out the scores 
    (Precision, Recall and F1-score for MUC, B^3, CEAF_m, CEAF_e and BLANC) + 
    (CoNLL-2012 average score). """
    # Osäker om det ska vara i den ordningen eller ('actualClusters', 'predictedClusters'), i beskrivningen står det (gold, sys). (tror att gold är predicted men osäker)
    output = ''.join(main.process_dirs('actualClusters', 'predictedClusters'))
    print(output)

if __name__ == "__main__":
    print_scores()