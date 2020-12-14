from preprocessing.output import example_x, example_y, random_data
from algorithm.model import Model
from algorithm.modelDt import ModelDT
from preprocessing.generateData import generate_training_data, generate_test_data
from evaluator import Evaluator, TestCase

def run_small():
    bob_is_bob = generate_test_data("./data/tests/bob_is_bob.tsv")[0]
    bob_is_erik = generate_test_data("./data/tests/bob_is_erik.tsv")[0]
    bob_is_not_erik = generate_test_data("./data/tests/bob_is_not_erik.tsv")[0]
    example = generate_test_data("./data/example/*.tsv")[0]

    num_features = bob_is_bob[0][0][0][1].shape[0]
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

    bob_is_bob_training = generate_training_data("./data/tests/bob_is_bob.tsv")[0]
    bob_is_erik_training = generate_training_data("./data/tests/bob_is_erik.tsv")[0]
    bob_is_not_erik_training = generate_training_data("./data/tests/bob_is_not_erik.tsv")[0]
    example_training = generate_training_data("./data/example/*.tsv")[0]

    training_data = [bob_is_bob_training, bob_is_erik_training, bob_is_not_erik_training, example_training]
    model = Model(training_data)
    model.train()
    model_dt = ModelDT(training_data)
    model_dt.train()

    evaluator = Evaluator()
    evaluator.add_case(TestCase(*bob_is_bob))
    evaluator.add_case(TestCase(*bob_is_erik))
    evaluator.add_case(TestCase(*bob_is_not_erik))
    (x1, y1) = random1
    # Pass an empty set and a name manually, as the random data has no name or mapping.
    evaluator.add_case(TestCase(x1, y1, {}, "random1"))
    (x2, y2) = random2
    evaluator.add_case(TestCase(x2, y2, {}, "random2"))
    evaluator.add_case(TestCase(*example))

    print("Normal model")
    evaluator.evaluate(model)
    print("Decision tree model")
    evaluator.evaluate(model_dt)

def run_big():
    training_data = generate_training_data("./data/GUM_tsv/trainingandval/*.tsv")

    num_features = training_data[0][0][0][0][1].shape[0]
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

    model = Model(training_data)
    model.train()

    testing_data = generate_test_data("./data/GUM_tsv/testing/*.tsv")

    evaluator = Evaluator()
    evaluator.print_translation = False
    for data in testing_data:
        evaluator.add_case(TestCase(*data))

    evaluator.evaluate(model)

if __name__ == '__main__':
    #run_small()
    run_big()
