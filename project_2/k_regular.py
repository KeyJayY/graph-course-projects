import random
import networkx as nx
import matplotlib.pyplot as plt

def generate_k_regular_graph_manual(n, k):
    if (n * k) % 2 != 0:
        raise ValueError("n * k musi być parzyste, aby graf istniał!")
    if k >= n:
        raise ValueError("Stopień k musi być mniejszy niż liczba wierzchołków n!")

    G = nx.Graph()
    G.add_nodes_from(range(n))

    # Lista stopni do spełnienia
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

                # Dodaj krawędź
                G.add_edge(u, v)
                degree_remaining[u] -= 1
                degree_remaining[v] -= 1
                connected = True
                break

            if connected:
                break

        if not connected:
            # Jeśli nie udało się połączyć, restartujemy (bo może być sytuacja bez wyjścia)
            return generate_k_regular_graph_manual(n, k)

    return G

def visualize_graph(G):
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color='lightgreen', node_size=800, font_size=12)
    plt.title("Samodzielnie wygenerowany k-regularny graf")
    plt.show()

if __name__ == '__main__':
    n = 10  # liczba wierzchołków
    k = 4   # stopień każdego wierzchołka

    G = generate_k_regular_graph_manual(n, k)
    visualize_graph(G)

    print("Krawędzie grafu:")
    print(list(G.edges()))
