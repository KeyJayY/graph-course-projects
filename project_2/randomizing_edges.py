from matplotlib import pyplot as plt
import random
import networkx as nx
from project_1.generator import *  # zakładam, że masz tam generate_random_graph_nl()

if __name__=='__main__':
    # Generowanie grafu
    G = generate_random_graph_nl(10, 15)

    # Rysowanie grafu przed zmianą
    nx.draw(G, with_labels=True, node_color='skyblue', node_size=800, font_size=12)
    plt.title("Graf przed zmianą krawędzi")
    plt.show()

    # Wybieramy losowe krawędzie
    random_edge_1 = random.choice(list(G.edges()))
    random_edge_3 = random.choice(list(G.edges()))

    # Wybieramy losowe końce krawędzi jako wierzchołki (z krotek)
    u1, v1 = random_edge_1
    u3, v3 = random_edge_3

    # Wybieramy losowy koniec jako punkt startowy
    node1 = random.choice([u1, v1])
    node3 = random.choice([u3, v3])

    # Wybieramy losowych sąsiadów dla tych wierzchołków
    neighbors1 = list(G.neighbors(node1))
    neighbors3 = list(G.neighbors(node3))

    # Upewniamy się, że nie próbujemy połączyć z samym sobą lub powtórzyć tej samej krawędzi
    if neighbors1 and neighbors3:
        node2 = random.choice(neighbors1)
        node4 = random.choice(neighbors3)

        G.remove_edge(node1, node2)
        G.remove_edge(node3, node4)

        G.add_edge(node1, node4)
        G.add_edge(node2, node3)

        print(f"Zamieniono: ({node1}, {node2}) → ({node1}, {node4})")
        print(f"Zamieniono: ({node3}, {node4}) → ({node2}, {node3})")

    # Rysowanie grafu po zamianie
    nx.draw(G, with_labels=True, node_color='skyblue', node_size=800, font_size=12)
    plt.title("Graf po zamianie krawędzi")
    plt.show()
