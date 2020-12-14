import numpy as np
import random

# Ändra här så mycket ni vill, så anpassar vi vår kod
# vi lade den här koden här så att vi kan koppla ihop
# våra delar sen.

# Beskriver grafen som adjacency list
example_x = \
[
  [ # node 0
    (1, np.array([1, 2, 3, 4])),
    (2, np.array([-1, -2, -3, -4]))
  ],
  [ # node 1
    (2, np.array([1, 0, 1, 0]))
  ],
  [], # node 2
]

# Beskriver vilka som är i samma coreference kluster
example_y = [0, 1, 0]

# Testar med två features [string matching headword, edit distance headword]
example_features_x = \
[
  [ # node 0
    (4, np.array([1, 0])),
    (1, np.array([0, 5])),
    (2, np.array([0, 4]))
  ],
  [ # node 1
    (4, np.array([0, 3])),
    (5, np.array([1, 0]))
  ],
  [ # node 2
    (6, np.array([0, 5]))
  ],
  [ # node 3
    (5, np.array([0, 4]))
  ],
  [ # node 4
    (6, np.array([1, 0]))
  ],
  [ # node 5
    (2, np.array([1, 0]))
  ],
  [ # node 6
    (3, np.array([1, 0]))
  ]
]

example_features_y = [0, 1, 1, 0, 0, 1, 0]

def random_data(node_count, cluster_count, features, max_edges):
  x = []
  y = list(range(cluster_count)) + \
      [random.randrange(cluster_count)
          for _ in range(node_count - cluster_count)]
  random.shuffle(y)

  all_nodes = list(range(node_count))
  for u in range(node_count):
    edges = []
    if not u == node_count - 1:
      for v in set(random.randrange(u+1, node_count) for _ in range(max_edges)):
        edges.append((v, np.random.normal(0, 1, features)))
    x.append(edges)

  return x, y