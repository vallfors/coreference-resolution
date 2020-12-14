import numpy as np

def mean_and_variance(edge_lists):
  large_list = np.concatenate(edge_lists)
  mean = np.mean(large_list, axis=0)
  variance = np.std(large_list, axis=0)
  variance[variance == 0] = 1
  return mean, variance

def normalize(edge_list, mean, variance):
  edge_list -= mean
  edge_list /= variance
