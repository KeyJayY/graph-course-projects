import networkx as nx


def components_R(nr, i, G, connected_graph_list):
    for j in G.neighbors(i):
        if connected_graph_list[j] == -1:
            connected_graph_list[j] = nr
            components_R(nr, j, G, connected_graph_list)

def connected_components_R(G):
    connected_graph_list = [-1 for _ in range(G.number_of_nodes())]
    nr = 0

    for i in range(G.number_of_nodes()):
        if connected_graph_list[i] == -1:
            nr += 1
            connected_graph_list[i] = nr
            components_R(nr, i, G, connected_graph_list)
    return connected_graph_list

if __name__ == '__main__':
    G = nx.Graph()
    G.add_edges_from([(0, 1), (1, 2)])
    G.add_edges_from([(3, 4), (4, 5), (5, 3)])

    connected_graph_list=connected_components_R(G)
    print("Składowe spójności (numer komponentu dla każdego wierzchołka):")
    print(connected_graph_list)
