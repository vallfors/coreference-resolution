import numpy as np
from .normalization import mean_and_variance, normalize
from .edmonds import mst as edmonds
from .featureInduction import generate_templates, append_induced_features
from collections import defaultdict

class Model:
  ROOT = -1
  ROOT_LOSS_VALUE = 1.5

  # Receive graph from preprocessing
  def __init__(self, training_data):
    self.training_data = training_data

  def train(self):
    self.templates = generate_templates(self.training_data)

    edge_lists = [self.__input_to_edge_list(x) for x, _ in self.training_data]

    features_list = [edge_list[0] for edge_list in edge_lists]
    self.mean, self.variance = mean_and_variance(features_list)
    for edge_list_features in features_list:
      normalize(edge_list_features, self.mean, self.variance)
    
    self.num_features = self.training_data[0][0][0][0][1].shape[0] + len(self.templates)
    self.weights = np.random.normal(0, 1, self.num_features)
    print("#features", self.num_features)

    convergence = False
    iteration_count = 0
    epochs = 1000
    for t in range(epochs):
      iteration_count += 1
    
      if convergence:
        break

      convergence = True
      for edge_list, (x, y) in zip(edge_lists, self.training_data):

        edge_list_features, edge_list_nodes, node_set = edge_list

        # break after convergence

        # Multiply edge list (matrix) with weights
        # edge_list_weights has shape (num_edges,)
        edge_list_weights = edge_list_features.dot(self.weights)

        # Convert edge list to adjacency list of the constrained graph
        constrained_graph = self.__edge_to_adjacency_list(
            edge_list_weights,
            edge_list_nodes,
            node_set,
            cluster_ids = y)

        # Insert adjacency list into edmonds algorithm, which returns 
        # h_tilde (an adjacency list)
        h_tilde = edmonds(self.ROOT, constrained_graph)

        # Convert edge list to adjacency list of the unconstrained graph
        graph_with_loss = self.__edge_to_adjacency_list(
            edge_list_weights,
            edge_list_nodes,
            node_set,
            h_tilde = h_tilde)
        # Insert adjacency list into edmonds algorithm, which returns
        # h_hatt (an adjacency list)
        h_hatt = edmonds(self.ROOT, graph_with_loss)
        
        # TODO: Convert h_tilde and h_hat back to edge lists
        # We also need to remove the edges to root node
        indices = []
        for u in h_tilde:
          for v in h_tilde[u]:
            if u == -1 or v == -1:
              break
            indices.append(edge_list_nodes.index((u, v)))
        h_tilde_features = edge_list_features[indices]


        indices = []
        for u in h_hatt:
          for v in h_hatt[u]:
            if u == -1 or v == -1:
              break
            indices.append(edge_list_nodes.index((u, v)))
        h_hatt_features = edge_list_features[indices]

        # Sum of features present in h_tilde (1d array)
        phi_h_tilde = h_tilde_features.sum(axis=0)

        # Sum of features present in h_hatt (1d array)
        phi_h_hatt = h_hatt_features.sum(axis=0)
        
        # TODO: Check for convergence
        #if sum(phi_h_tilde - phi_h_hatt) == 0:
        #  break

        delta = phi_h_tilde - phi_h_hatt
        #print("Iteration", iteration_count, "delta:", delta.sum())
        if delta.sum() != 0:
          convergence = False

        # TODO: Update weights to weights + phi(x, h_tilde) - phi(x, h_hat)
        learning_rate_init = 1
        #decay_rate = learning_rate_init / epochs
        decay_rate = 1/100
        learning_rate = learning_rate_init / (1 + decay_rate*t)
        self.weights = self.weights + learning_rate*delta
      
    print("Done training in", iteration_count, "iterations.")
   
  # Returns the cluster id's.
  def classify(self, x):
    edge_list_features, edge_list_nodes, node_set = \
        self.__input_to_edge_list(x)
    normalize(edge_list_features, self.mean, self.variance)
    
    edge_list_weights = edge_list_features.dot(self.weights)
    graph = self.__edge_to_adjacency_list(
        edge_list_weights, edge_list_nodes, node_set)
    h = edmonds(self.ROOT, graph)

    cluster_ids = [0]*len(node_set)

    def dfs(node, cluster_id):
      cluster_ids[node] = cluster_id
      if not node in h:
        return
      for child in h[node]:
        dfs(child, cluster_id)

    for i, subtree_root in enumerate(h[self.ROOT]):
      dfs(subtree_root, i)

    return cluster_ids

  def __input_to_edge_list(self, x):
    # 2D-matrix [#edges][#features] -> feature
    edge_list_features = [] 
    # 1D-matrix [#edges] -> (origin node, destination node)
    edge_list_nodes = []
    # Set of all nodes
    node_set = list(range(len(x)))

    # Convert graph to edge list
    for u, edges in enumerate(x):
      for v, features in edges:
        edge_list_features.append(append_induced_features(features, self.templates))
        edge_list_nodes.append((u, v))

    edge_list_features = np.array(edge_list_features)

    return edge_list_features, edge_list_nodes, node_set

  def __edge_to_adjacency_list(self,
      edge_list_weights,
      edge_list_nodes,
      node_set,
      cluster_ids=None,
      h_tilde=None):

    adjacency_list = defaultdict(dict)
    # Connect all nodes to Root
    for u in node_set:
      adjacency_list[self.ROOT][u] = 0 if h_tilde == None else -self.ROOT_LOSS_VALUE

    for weight, nodes in zip(edge_list_weights, edge_list_nodes):
      u, v = nodes

      # Constrain graph
      if cluster_ids != None and cluster_ids[u] != cluster_ids[v]:
        continue

      # Apply loss function. Add 1 to each edge in adjacency list not 
      # present in h_tilde
      if h_tilde != None and \
          (not u in h_tilde or not v in h_tilde[u]):
        if not u == self.ROOT and not v == self.ROOT:
          weight += 1

      # The implementation calculates. Minimum ST. Multiply weight
      # by -1 to get maximum. Adds edge with weight to adjacency list.
      adjacency_list[u][v] = -weight
    return adjacency_list

