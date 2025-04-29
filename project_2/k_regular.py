import random
import networkx as nx
from project_1.draw_graph import draw_circle_graph


def generate_k_regular_graph_manual(n, k):
    """
    Funkcja generująca graf k-regularny, czyli graf, w którym każdy wierzchołek ma stopień równy k.

    :param n: liczba wierzchołków w grafie
    :param k: stopień każdego wierzchołka
    :return: graf k-regularny
    :raises ValueError: jeśli n * k nie jest liczbą parzystą lub jeśli k >= n
    """
    if (n * k) % 2 != 0:
        raise ValueError("n * k musi być parzyste, aby graf istniał!")

    if k >= n:
        raise ValueError("Stopień k musi być mniejszy niż liczba wierzchołków n!")

    G = nx.Graph()
    G.add_nodes_from(range(n))

    degree_remaining = {i: k for i in range(n)}
    nodes = list(G.nodes())

    while any(degree_remaining.values()):
        random.shuffle(nodes)

        connected = False

        for i in range(n):
            u = nodes[i]
            if degree_remaining[u] == 0:
                continue
            for j in range(i + 1, n):
                v = nodes[j]
                if degree_remaining[v] == 0 or G.has_edge(u, v) or u == v:
                    continue

                G.add_edge(u, v)
                degree_remaining[u] -= 1
                degree_remaining[v] -= 1
                connected = True
                break

            if connected:
                break
        if not connected:
            return generate_k_regular_graph_manual(n, k)

    return G



def main():
    """
    Funkcja główna programu, która generuje graf k-regularny, rysuje go i wypisuje jego krawędzie.
    """
    n = 10
    k = 4

    G = generate_k_regular_graph_manual(n, k)

    draw_circle_graph(G, radius=10, name="k_regular_graph.png", weights=False)

    print("Krawędzie grafu:")
    print(list(G.edges()))


if __name__ == '__main__':
    main()
