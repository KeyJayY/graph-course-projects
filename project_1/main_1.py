from draw_graph import *
from converter import *
from generator import *


def task1():
    G = nx.Graph()
    G.add_edges_from([(1, 2), (2, 3), (3, 4), (4, 1), (1, 3)])

    adj_matrix = graph_to_adjacency_matrix(G)
    inc_matrix = graph_to_incidence_matrix(G)
    adj_list = graph_to_adjacency_list(G)

    print("Macierz sąsiedztwa:\n", adj_matrix)
    print("\nMacierz incydencji:\n", inc_matrix)
    print("\nLista sąsiedztwa:\n", adj_list)

    G_from_adj_matrix = adjacency_matrix_to_graph(adj_matrix)
    G_from_inc_matrix = incidence_matrix_to_graph(inc_matrix)
    G_from_adj_list = adjacency_list_to_graph(adj_list)

    print("\nGraf odtworzony z macierzy sąsiedztwa:", G_from_adj_matrix.edges())
    print("\nGraf odtworzony z macierzy incydencji:", G_from_inc_matrix.edges())
    print("\nGraf odtworzony z listy sąsiedztwa:", G_from_adj_list.edges())

    draw_circle_graph(G_from_adj_matrix, 5, "adj_matrix")
    draw_circle_graph(G_from_inc_matrix, 5, "inc_matrix")
    draw_circle_graph(G_from_adj_list, 5, "adj_list")


def task3():
    G = generate_random_graph_nl(5, 10)
    G2 = generate_random_graph_np(5, 0.5)
    draw_circle_graph(G, 5, "random_graph_nl")
    draw_circle_graph(G2, 5, "random_graph_np")


if __name__ == "__main__":
    task1()
    task3()
