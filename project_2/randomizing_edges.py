import random
from project_1.generator import generate_random_graph_nl
from project_1.draw_graph import draw_circle_graph


def generate_and_draw_graph(n_nodes, n_edges, name_before):
    """
    Generuje graf o zadanej liczbie wierzchołków (n_nodes) i krawędzi (n_edges),
    a następnie zapisuje jego obraz przed randomizacją.

    :param n_nodes: liczba wierzchołków w grafie
    :param n_edges: liczba krawędzi w grafie
    :param name_before: nazwa pliku, w którym zapisujemy obraz grafu przed randomizacją
    :return: obiekt grafu (G)
    """
    G = generate_random_graph_nl(n_nodes, n_edges)
    draw_circle_graph(G, radius=10, name=name_before)
    return G


def randomize_edges(G, randomizations):
    """
    Funkcja losowo modyfikuje krawędzie w grafie, przeprowadzając dokładnie `randomizations` skutecznych zamian.
    W każdej zamianie wybieramy dwie krawędzie, usuwamy je i dodajemy nowe krawędzie, upewniając się, że
    nie są to pętle ani wielokrotne krawędzie.

    :param G: graf, którego krawędzie mają zostać zrandomizowane
    :param randomizations: liczba zamian krawędzi
    :return: zmodyfikowany graf
    """
    successful_swaps = 0
    max_attempts = randomizations * 10
    attempts = 0

    # Pętla wykonująca zamiany krawędzi
    while successful_swaps < randomizations and attempts < max_attempts:
        attempts += 1

        edges = list(G.edges())
        if len(edges) < 2:
            break

        random_edge_1 = random.choice(edges)
        random_edge_2 = random.choice(edges)

        u1, v1 = random_edge_1
        u2, v2 = random_edge_2

        a, b = random.choice([(u1, v1), (v1, u1)])
        c, d = random.choice([(u2, v2), (v2, u2)])

        if a != d and b != c and not G.has_edge(a, d) and not G.has_edge(b, c):
            G.remove_edge(a, b)
            G.remove_edge(c, d)
            G.add_edge(a, d)
            G.add_edge(b, c)

            successful_swaps += 1
            print(
                f"[{successful_swaps}] Zamieniono: ({a}, {b}) + ({c}, {d}) → ({a}, {d}) + ({b}, {c})"
            )

    if successful_swaps < randomizations:
        print(
            f"Ostrzeżenie: Wykonano tylko {successful_swaps} z {randomizations} zamian."
        )

    return G


def main():
    """
    Główna funkcja programu, która generuje graf, randomizuje krawędzie,
    a następnie rysuje graf przed i po randomizacji.
    """
    n_nodes = 10
    n_edges = 15
    randomizations = 3
    G = generate_and_draw_graph(n_nodes, n_edges, "graph_before_randomization.png")
    G = randomize_edges(G, randomizations)
    draw_circle_graph(G, radius=10, name="graph_after_randomization.png")


if __name__ == "__main__":
    main()
