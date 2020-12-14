import numpy as np
from sklearn.tree import DecisionTreeClassifier

class ModelDT:

  # Receive graph from preprocessing
  def __init__(self, training_data):
    self.training_data = training_data

  def train(self):
    x = []
    y = []

    for graph, cluster_id in self.training_data:
      for u, edges in enumerate(graph):
        for v, features in edges:
          x.append(features)
          y.append(1 if cluster_id[u] == cluster_id[v] else 0)
    
    x = np.array(x)
    y = np.array(y)


    estimator = DecisionTreeClassifier(random_state=0, max_depth=3)
    self.estimator = estimator.fit(x, y)
   
  # Returns the cluster id's.
  def classify(self, x):
    adj = [[] for _ in range(len(x))]

    for u, edges in enumerate(x):
      for v, features in edges:
        if self.estimator.predict(np.array([features]))[0] == 1:
          adj[u].append(v)
          adj[v].append(u)

    y = [-1]*len(x)

    def dfs(u, id):
      if y[u] != -1:
        return
      y[u] = id
      for v in adj[u]:
        dfs(v, id)

    cluster_id = 0
    for i in range(len(x)):
      if y[i] == -1:
        dfs(i, cluster_id)
        cluster_id += 1

    return y

