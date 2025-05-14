import random


def generate_random_digraph_adjacency_matrix(n, p):
    """
    Generuje losowy graf skierowany z n wierzchołkami i prawdopodobieństwem p dla każdej krawędzi.
    :param n: liczba wierzchołków
    :param p: prawdopodobieństwo dodania krawędzi między dwoma wierzchołkami
    :return: graf skierowany jako obiekt NetworkX DiGraph
    """
    matrix = [[0] * n for _ in range(n)]
    for u in range(n):
        for v in range(n):
            if u != v and random.random() < p:
                matrix[u][v] = 1
    return matrix


def add_weights_to_digraph(adjacency_matrix, min_weight=-5, max_weight=10):
    """
    Dodaje losowe wagi do krawędzi grafu skierowanego.
    :param adjacency_matrix: macierz sąsiedztwa grafu skierowanego
    :param min_weight: minimalna waga krawędzi
    :param max_weight: maksymalna waga krawędzi
    :return: macierz sąsiedztwa z wagami
    """
    n = len(adjacency_matrix)
    weighted_matrix = [[None] * n for _ in range(n)]
    for u in range(n):
        for v in range(n):
            if adjacency_matrix[u][v] == 1:
                weighted_matrix[u][v] = random.randint(min_weight, max_weight)
    return weighted_matrix
