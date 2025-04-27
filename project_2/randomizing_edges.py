import random
import networkx as nx
from project_1.generator import generate_random_graph_nl
from project_1.draw_graph import draw_circle_graph

def generate_and_draw_graph(n_nodes, n_edges, name_before):
    """Generuje graf i zapisuje jego obraz przed randomizacją."""
    G = generate_random_graph_nl(n_nodes, n_edges)
    draw_circle_graph(G, radius=10, name=name_before)
    return G

def randomize_edges(G, randomizations):
    """Randomizuje krawędzie w grafie."""
    for _ in range(randomizations):
        # Wybieramy dwie losowe krawędzie
        random_edge_1 = random.choice(list(G.edges()))
        random_edge_3 = random.choice(list(G.edges()))

        u1, v1 = random_edge_1
        u3, v3 = random_edge_3

        node1 = random.choice([u1, v1])
        node3 = random.choice([u3, v3])

        neighbors1 = list(G.neighbors(node1))
        neighbors3 = list(G.neighbors(node3))

        if neighbors1 and neighbors3:
            node2 = random.choice(neighbors1)
            node4 = random.choice(neighbors3)

            # Warunek: unikamy tworzenia pętli i wielokrotnych krawędzi
            if node1 != node4 and node2 != node3 and not G.has_edge(node1, node4) and not G.has_edge(node2, node3):
                G.remove_edge(node1, node2)
                G.remove_edge(node3, node4)
                G.add_edge(node1, node4)
                G.add_edge(node2, node3)
                print(f"Zamieniono: ({node1}, {node2}) → ({node1}, {node4})")
                print(f"Zamieniono: ({node3}, {node4}) → ({node2}, {node3})")
    return G

def main():
    n_nodes = 10
    n_edges = 15
    randomizations = 5  # liczba zamian krawędzi

    # Generujemy graf i rysujemy przed zamianami
    G = generate_and_draw_graph(n_nodes, n_edges, "graph_before_randomization.png")

    # Randomizujemy krawędzie
    G = randomize_edges(G, randomizations)

    # Rysujemy graf po randomizacji
    draw_circle_graph(G, radius=10, name="graph_after_randomization.png")

if __name__ == '__main__':
    main()
