import random
import networkx as nx
from project_1.draw_graph import draw_circle_graph

def generate_k_regular_graph_manual(n, k):
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

def visualize_graph(G, filename="k_regular_graph.png"):
    draw_circle_graph(G, radius=10, name=filename, weights=False)

def main():
    n = 10  # liczba wierzchołków
    k = 4   # stopień każdego wierzchołka

    G = generate_k_regular_graph_manual(n, k)
    visualize_graph(G, filename="k_regular_graph.png")

    print("Krawędzie grafu:")
    print(list(G.edges()))

if __name__ == '__main__':
    main()
