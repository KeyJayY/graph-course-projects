import networkx as nx


def convert_digraph_to_adjacency_matrix(digraph, weights=False):
    """
    Konwertuje graf skierowany na macierz sąsiedztwa.
    :param digraph: graf skierowany
    :return: macierz sąsiedztwa
    """
    num_nodes = digraph.number_of_nodes()
    adjacency_matrix = [[0] * num_nodes for _ in range(num_nodes)]

    for u, v in digraph.edges():
        if weights:
            weight = digraph[u][v]["weight"]
            adjacency_matrix[u][v] = weight
        else:
            adjacency_matrix[u][v] = 1

    return adjacency_matrix


def convert_adjacency_matrix_to_digraph(adjacency_matrix, weights=False):
    """
    Konwertuje macierz sąsiedztwa na graf skierowany.
    :param adjacency_matrix: macierz sąsiedztwa
    :return: graf skierowany
    """
    num_nodes = len(adjacency_matrix)
    digraph = nx.DiGraph()
    digraph.add_nodes_from(range(num_nodes))

    for i in range(num_nodes):
        for j in range(num_nodes):
            if weights:
                if adjacency_matrix[i][j] != None:
                    digraph.add_edge(i, j, weight=adjacency_matrix[i][j])
            else:
                if adjacency_matrix[i][j]:
                    digraph.add_edge(i, j)

    return digraph
