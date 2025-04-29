import random
import networkx as nx
from project_1.draw_graph import draw_circle_graph
from project_2.sequence_graph import havel_hakimi, build_graph

def generating_euler_graph(nodes_num):
    """
    Generuje graf Eulerowski na podstawie algorytmu Havel-Hakimi.
    Zwraca graf, który spełnia warunki grafu Eulerowskiego (spójny i każdemu wierzchołkowi przypisany parzysty stopień).
    """
    while True:
        sequence = []
        for _ in range(nodes_num):
            sequence.append(random.choice([i for i in range(2, nodes_num + 1, 2)]))

        if havel_hakimi(sequence):
            G = build_graph(sequence)
            if nx.is_connected(G) and all(d % 2 == 0 for _, d in G.degree()):
                print("Znaleziono sekwencję:", sequence)
                return G

def fleury_euler_graph(G):
    """
    Algorytm Fleury'ego do znalezienia cyklu Eulera w grafie.
    """
    if not nx.is_connected(G) or not nx.is_eulerian(G):
        print("Graf nie jest eulerowski!")
        return []

    G_copy = G.copy()
    current = list(G_copy.nodes())[0]
    path = [current]

    while G_copy.edges():
        neighbors = list(G_copy.neighbors(current))
        if not neighbors:
            break

        next_node = None
        for neighbor in neighbors:
            if len(neighbors) == 1:
                next_node = neighbor
                break
            else:
                G_copy.remove_edge(current, neighbor)
                if nx.is_connected(G_copy):
                    next_node = neighbor
                    G_copy.add_edge(current, neighbor)
                    break
                G_copy.add_edge(current, neighbor)

        if next_node is None:
            next_node = neighbors[0]
        G_copy.remove_edge(current, next_node)
        current = next_node
        path.append(current)

    return path

def main():
    """
    Główna funkcja programu – generuje graf Eulerowski, rysuje go i znajduje cykl Eulera.
    """
    G = generating_euler_graph(8)

    draw_circle_graph(G, radius=10, name="euler_graph.png", weights=False)

    path = fleury_euler_graph(G)
    print("Cykl Eulera:", path)

if __name__ == '__main__':
    main()
