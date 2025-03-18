import numpy as np
import networkx as nx


def graph_to_adjacency_matrix(G):
    """Zamienia graf NetworkX na macierz sąsiedztwa"""
    return nx.to_numpy_array(G, dtype=int)


def graph_to_incidence_matrix(G):
    """Zamienia graf NetworkX na macierz incydencji"""
    nodes = list(G.nodes())
    num_nodes = len(nodes)
    num_edges = len(G.edges())

    node_index = {node: i for i, node in enumerate(nodes)}
    incidence_matrix = np.zeros((num_nodes, num_edges), dtype=int)

    for edge_index, (u, v) in enumerate(G.edges()):
        incidence_matrix[node_index[u], edge_index] = 1
        incidence_matrix[node_index[v], edge_index] = 1

    return incidence_matrix


def graph_to_adjacency_list(G):
    """Zamienia graf NetworkX na listę sąsiedztwa"""
    return {node: list(G.neighbors(node)) for node in G.nodes()}


def adjacency_matrix_to_graph(matrix):
    """Konwertuje macierz sąsiedztwa na graf NetworkX"""
    G = nx.Graph()
    num_nodes = len(matrix)

    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            if matrix[i][j] == 1:
                G.add_edge(i + 1, j + 1)

    return G


def incidence_matrix_to_graph(matrix):
    """Konwertuje macierz incydencji na graf NetworkX"""
    G = nx.Graph()
    num_nodes, num_edges = matrix.shape

    for edge_index in range(num_edges):
        nodes = np.where(matrix[:, edge_index] == 1)[0]
        if len(nodes) == 2:
            G.add_edge(nodes[0] + 1, nodes[1] + 1)

    return G


def adjacency_list_to_graph(adj_list):
    """Konwertuje listę sąsiedztwa na graf NetworkX"""
    G = nx.Graph()
    for node, neighbors in adj_list.items():
        for neighbor in neighbors:
            if not G.has_edge(node, neighbor):
                G.add_edge(node, neighbor)
    return G