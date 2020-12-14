import networkx as nx
import numpy as np
import os
from printScores import save_scores_to_file, print_scores, save_mapping_to_file

def matching(predicted, actual):
  predicted_clusters = set(predicted)
  actual_clusters = set(actual)

  score = [[0]*len(actual_clusters) for _ in predicted_clusters]
  for p, a in zip(predicted, actual):
    score[p][a] += 1

  G = nx.Graph()
  for p in range(len(predicted_clusters)):
    for a in range(len(actual_clusters)):
      G.add_edge("p%s"%p, "a%s"%a, weight=score[p][a])
  matching = nx.max_weight_matching(G)

  matched = 0
  pa_dict = {}
  for p, a in zip(predicted, actual):
    p = "p%s"%p
    a = "a%s"%a
    if (p, a) in matching or (a, p) in matching:
      matched += 1
      pa_dict[int(p[1:])] = int(a[1:])

  return pa_dict

def translate(predicted, actual):

  pa_dict = matching(predicted, actual)
  predicted_translated = [0] * len(predicted)
  for i, p in enumerate(predicted):
    predicted_translated[i] = pa_dict[p] if p in pa_dict else -1

  return predicted_translated

def calculate_stats(predicted, actual):
  true_pos, false_pos, true_neg, false_neg = 0, 0, 0, 0

  for i in range(len(predicted)):
    for j in range(i+1, len(predicted)):
      if i == j:
        continue
      if actual[i] == actual[j]: # should be same
        if predicted[i] == predicted[j]:
          true_pos += 1
        else:
          false_neg += 1
      else: # should be different
        if predicted[i] == predicted[j]:
          false_pos += 1
        else:
          true_neg += 1

  accuracy, precision, recall = (0.00001,)*3
  if true_pos + true_neg > 0:
    accuracy = (true_pos + true_neg) / \
      (true_pos + true_neg + false_pos + false_neg)
  if true_pos > 0:
    precision = true_pos / (true_pos + false_pos)
    recall = true_pos / (true_pos + false_neg)
  if true_pos == 0 and false_neg == 0:
    recall = 1
  if true_pos == 0 and false_pos == 0:
    precision = 1
  f1 = 2*precision*recall / (precision + recall)
  return accuracy, precision, recall, f1

class TestCase:
  def __init__(self, x, y, id_to_position, filename):
    base = os.path.basename(filename)
    self.name = os.path.splitext(base)[0]
    self.x = x
    self.y = y
    self.id_to_position = id_to_position

class Evaluator:
  print_translation = True

  def __init__(self):
    self.__test_cases = []

  def add_case(self, case):
    self.__test_cases.append(case)

  def __print(self, name, accuracy, precision, recall, f1):
    print("Case {:>15}:\tF1 {:.3f} \tAccuracy: {:.3f} \tPrecision: {:.3f} \tRecall: {:.3f}" \
        .format(name, f1, accuracy, precision, recall))

  def evaluate(self, model):
    scores = []
    for case in self.__test_cases:
      predicted = model.classify(case.x)
      actual = case.y

      save_scores_to_file(case.name, actual, predicted)
      save_mapping_to_file(case.name, case.id_to_position)
    print_scores()
    """
      accuracy, precision, recall, f1 = calculate_stats(predicted, actual)
      self.__print(case.name, accuracy, precision, recall, f1)
      if self.print_translation:
        #translated = translate(predicted, actual)
        #print(" Actual clusters:     {}\n Translated clusters: {}\n Predicted clusters:  {}".format(
         # "".join(["{:3d},".format(i) for i in actual]),
          #"".join(["{:3d},".format(i) for i in translated]),
          #"".join(["{:3d},".format(i) for i in predicted])))
        print(" Actual clusters:     {}\n Predicted clusters:  {}".format(
          "".join(["{:3d},".format(i) for i in actual]),
          "".join(["{:3d},".format(i) for i in predicted])))
      scores.append([accuracy, precision, recall, f1])

    scores = np.array(scores)
    scores = np.mean(scores, axis=0)
    self.__print("Average", *(scores.tolist()))
    """

