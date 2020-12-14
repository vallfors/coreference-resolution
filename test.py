from preprocessing.output import random_data
from algorithm.model import Model
from evaluator import Evaluator, TestCase

num_features = 100
training1 = random_data(
    node_count=10,
    cluster_count=2,
    features=num_features,
    max_edges=30)
training2 = random_data(
    node_count=10,
    cluster_count=2,
    features=num_features,
    max_edges=30)
random1 = random_data(
    node_count=10,
    cluster_count=2,
    features=num_features,
    max_edges=30)
random2 = random_data(
    node_count=10,
    cluster_count=2,
    features=num_features,
    max_edges=30)

training_data = [training1, training2]
model = Model(training_data)
model.train()

evaluator = Evaluator()
evaluator.add_case(TestCase("Training 1", *training1))
evaluator.add_case(TestCase("Training 2", *training2))
evaluator.add_case(TestCase("Random 1", *random1))
evaluator.add_case(TestCase("Random 2", *random2))

evaluator.evaluate(model)