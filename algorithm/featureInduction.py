from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import export_text
from sklearn.tree import export_graphviz
import numpy as np
from preprocessing.features import basic_features

class Question:
    def __init__(self, feature_id, threshold, greater_than):
        self.feature_id = feature_id
        self.threshold = threshold
        self.greater_than = greater_than
    
    def __str__(self):
        return "feature_{} {} {}".format(self.feature_id, ">" if self.greater_than else "<=", self.threshold)

    def passes_question(self, features):
        return self.greater_than == features[self.feature_id] > self.threshold

def append_induced_features(features, templates):
    for template in templates:
        result = 1
        for question in template:
            if not question.passes_question(features):
                result = 0
                break
        features = np.append(features, result)
    return features

def generate_templates(training_data):
    x = []
    y = []

    for graph, cluster_id in training_data:
        for u, edges in enumerate(graph):
            for v, features in edges:
                x.append(features)
                y.append(1 if cluster_id[u] == cluster_id[v] else 0)
    
    x = np.array(x)
    y = np.array(y)
    print(x)
    print(y)


    estimator = DecisionTreeClassifier(random_state=0, max_depth=3)
    estimator = estimator.fit(x, y)
    print(export_text(estimator))

    n_nodes = estimator.tree_.node_count
    children_left = estimator.tree_.children_left
    children_right = estimator.tree_.children_right
    feature = estimator.tree_.feature
    threshold = estimator.tree_.threshold

    templates = []
    def dfs(node, template_prefix, is_root = False):
        if template_prefix != []:
            templates.append(template_prefix)

        left, right = children_left[node], children_right[node]
        if left != -1:
            question = Question(feature[node], threshold[node], False)
            if is_root:
                dfs(left, [])
            dfs(left, template_prefix.copy() + [question])

        if right != -1:
            question = Question(feature[node], threshold[node], True)
            if is_root:
                dfs(right, [])
            dfs(right, template_prefix.copy() + [question])
    
    dfs(0, [], is_root=True)
    print("Feature induction templates:")
    for template in templates:
        print (", ".join([str(question) for question in template]))


    labels = []
    for f in basic_features:
        labels.append(f.__name__)
    print(export_text(estimator, labels))

    return templates
    
    

