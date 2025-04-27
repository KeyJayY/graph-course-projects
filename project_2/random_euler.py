from connected_graph import *
from randomizing_edges import *
from sequence_graph import *


def generating_euler_graph(nodes_num):
    while True:
        sequence=[random.randrange(0, nodes_num, 2) for n in range(nodes_num)]
        if havel_hakimi(sequence):
            G=build_graph(sequence)
            return G

def is_bridge(G, u, v):
    """Sprawdza, czy krawędź (u,v) jest mostem"""
    G_copy = G.copy()
    G_copy.remove_edge(u, v)
    return not nx.is_connected(G_copy)

def fleury_euler_graph(G):
    if not nx.is_connected(G) or not nx.is_eulerian(G):
        print("Graf nie jest eulerowski!")
        return []

    G_copy = G.copy()
    current = list(G_copy.nodes())[0]
    path = [current]

    while G_copy.edges():
        neighbors = list(G_copy.neighbors(current))

        # Wybieramy krawędź, która nie jest mostem, jeśli to możliwe
        for neighbor in neighbors:
            if len(neighbors) == 1 or not is_bridge(G_copy, current, neighbor):
                G_copy.remove_edge(current, neighbor)
                current = neighbor
                path.append(current)
                break

    return path



if __name__ == '__main__':
    G = nx.Graph()
    G=generating_euler_graph(6)
    visualize_graph(G)
    path=fleury_euler_graph(G)
    print(path)


