import random
import numpy as np
import random


def generate_weighted_connected_graph_nl(n, l):
    """Generuje spójną losową macierz sąsiedztwa dla grafu G(n, l) z wagami krawędzi."""
    if l < n - 1:
        raise ValueError(
            "Liczba krawędzi musi być co najmniej n-1, aby graf był spójny."
        )

    adj_matrix = np.zeros((n, n), dtype=int)

    nodes = list(range(n))
    random.shuffle(nodes)

    for i in range(n - 1):
        weight = random.randint(1, 10)
        adj_matrix[nodes[i], nodes[i + 1]] = weight
        adj_matrix[nodes[i + 1], nodes[i]] = weight

    possible_edges = [
        (i, j) for i in range(n) for j in range(i + 1, n) if adj_matrix[i, j] == 0
    ]
    random.shuffle(possible_edges)

    extra_edges = min(l - (n - 1), len(possible_edges))
    for i in range(extra_edges):
        weight = random.randint(1, 10)
        u, v = possible_edges[i]
        adj_matrix[u, v] = weight
        adj_matrix[v, u] = weight

    return adj_matrix
