import networkx as nx
import random


def generate_random_graph_nl(n, l):
    """Generuje losowy graf G(n, l) o 'n' wierzchołkach i  l krawędziach."""
    G = nx.Graph()
    G.add_nodes_from(range(1, n + 1))

    possible_edges = [(i, j) for i in range(1, n + 1) for j in range(i + 1, n + 1)]
    random_edges = random.sample(possible_edges, min(l, len(possible_edges)))

    G.add_edges_from(random_edges)
    return G


def generate_random_graph_np(n, p):
    """Generuje losowy graf G(n, p) o 'n' wierzchołkach, gdzie każda krawędź pojawia się z prawdopodobieństwem p."""
    G = nx.Graph()
    G.add_nodes_from(range(1, n + 1))

    for i in range(1, n + 1):
        for j in range(i + 1, n + 1):
            if random.random() < p:
                G.add_edge(i, j)

    return G