import numpy as np
import networkx as nx


def graph_to_adjacency_matrix(G):
    """
    Zamienia graf NetworkX na macierz sąsiedztwa (ręczna implementacja).

    Parametry:
        G (nx.Graph): Graf nieskierowany.

    Zwraca:
        np.ndarray: Kwadratowa macierz sąsiedztwa typu int.
    """
    if not isinstance(G, nx.Graph):
        raise TypeError("Input must be a NetworkX Graph")

    if len(G.nodes()) == 0:
        return np.zeros((0, 0), dtype=int)

    nodes = list(G.nodes())
    n = len(nodes)
    node_index = {node: i for i, node in enumerate(nodes)}
    matrix = np.zeros((n, n), dtype=int)

    for u, v in G.edges():
        i, j = node_index[u], node_index[v]
        matrix[i][j] = 1
        matrix[j][i] = 1

    return matrix


def graph_to_incidence_matrix(G):
    """
    Zamienia graf NetworkX na macierz incydencji.

    Parametry:
        G (nx.Graph): Graf nieskierowany.

    Zwraca:
        np.ndarray: Macierz incydencji (n wierzchołków x m krawędzi).
    """
    if not isinstance(G, nx.Graph):
        raise TypeError("Input must be a NetworkX Graph")

    if len(G.nodes()) == 0 or len(G.edges()) == 0:
        return np.zeros((0, 0), dtype=int)

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
    """
    Zamienia graf NetworkX na listę sąsiedztwa.

    Parametry:
        G (nx.Graph): Graf nieskierowany.

    Zwraca:
        dict: Słownik {wierzchołek: [lista sąsiadów]}.
    """
    if not isinstance(G, nx.Graph):
        raise TypeError("Input must be a NetworkX Graph")

    return {node: list(G.neighbors(node)) for node in G.nodes()}


def adjacency_matrix_to_graph(matrix):
    """
    Konwertuje macierz sąsiedztwa na graf NetworkX.

    Parametry:
        matrix (list lub np.ndarray): Kwadratowa macierz sąsiedztwa.

    Zwraca:
        nx.Graph: Odtworzony graf.
    """
    if matrix is None:
        raise ValueError("Matrix cannot be None")
    if not isinstance(matrix, (np.ndarray, list)):
        raise TypeError("Input must be a numpy array or nested list")

    matrix = np.array(matrix)
    if matrix.size == 0:
        return nx.Graph()
    if matrix.shape[0] != matrix.shape[1]:
        raise ValueError("Adjacency matrix must be square")

    G = nx.Graph()
    num_nodes = matrix.shape[0]

    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            if matrix[i][j] > 0:
                G.add_edge(i + 1, j + 1, weight=matrix[i][j])

    return G


def incidence_matrix_to_graph(matrix):
    """
    Konwertuje macierz incydencji na graf NetworkX.

    Parametry:
        matrix (list lub np.ndarray): Macierz incydencji (n wierzchołków x m krawędzi).

    Zwraca:
        nx.Graph: Odtworzony graf.
    """
    if matrix is None:
        raise ValueError("Matrix cannot be None")
    if not isinstance(matrix, (np.ndarray, list)):
        raise TypeError("Input must be a numpy array or nested list")

    matrix = np.array(matrix)
    if matrix.ndim != 2:
        raise ValueError("Incidence matrix must be 2D")
    if matrix.size == 0 or matrix.shape[1] == 0:
        return nx.Graph()

    G = nx.Graph()
    num_nodes, num_edges = matrix.shape

    for edge_index in range(num_edges):
        nodes = np.where(matrix[:, edge_index] == 1)[0]
        if len(nodes) == 2:
            G.add_edge(nodes[0] + 1, nodes[1] + 1)
        elif len(nodes) > 2:
            raise ValueError(f"Edge index {edge_index} connects more than two nodes")

    return G


def adjacency_list_to_graph(adj_list):
    """
    Konwertuje listę sąsiedztwa na graf NetworkX.

    Parametry:
        adj_list (dict): Słownik {wierzchołek: [lista sąsiadów]}.

    Zwraca:
        nx.Graph: Odtworzony graf.
    """
    if adj_list is None:
        raise ValueError("Adjacency list cannot be None")
    if not isinstance(adj_list, dict):
        raise TypeError("Adjacency list must be a dictionary")
    if len(adj_list) == 0:
        return nx.Graph()

    G = nx.Graph()
    for node, neighbors in adj_list.items():
        if not isinstance(neighbors, list):
            raise TypeError(f"Neighbors of node {node} must be in a list")
        for neighbor in neighbors:
            G.add_edge(node, neighbor)
    return G
