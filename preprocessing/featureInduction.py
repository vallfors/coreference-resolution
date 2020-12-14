from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import export_text
from sklearn.tree import export_graphviz
import numpy as np

iris = load_iris()
estimator = DecisionTreeClassifier(random_state=0, max_depth=2)
estimator = estimator.fit(iris.data, iris.target)
r = export_text(estimator, feature_names=iris['feature_names'])
g = export_graphviz(estimator)
print(r)
print(estimator.tree_.children_left)

n_nodes = estimator.tree_.node_count
children_left = estimator.tree_.children_left
children_right = estimator.tree_.children_right
feature = estimator.tree_.feature
threshold = estimator.tree_.threshold

path = {}
path[0] = [0]
MAX_DEPTH = 4

def dfs(id, depth):
    if depth >= MAX_DEPTH:
        return
    if (children_left[id] != -1):
        path[children_left[id]] = path[id].copy()
        path[children_left[id]].append(children_left[id])
        dfs(children_left[id], depth+1)

    if (children_right[id] != -1):
        path[children_right[id]] = path[id].copy()
        path[children_right[id]].append(children_right[id])
        dfs(children_right[id], depth+1)

dfs(0, 0)
print(path)


def feature_induction(mentions):
    graph = []
    number_of_mentions = len(mentions)
    number_of_sentences = mentions[number_of_mentions-1].sentence
    for i in range(number_of_mentions):
        neighbours = []
        for j in range(i+1, number_of_mentions):
            for f in basic_features:
                feature_vector.append(f(m_i, m_j))
            datapoints.append((feature_vector, answer))
        graph.append(neighbours)
    return graph