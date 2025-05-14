from project_1.draw_graph import draw_circle_graph
from project_4.generator import (
    generate_random_digraph_adjacency_matrix,
    add_weights_to_digraph,
)
from project_4.converter import convert_adjacency_matrix_to_digraph
from project_4.algorithms import (
    kosaraju,
    bellman_ford,
    johnson,
)


if __name__ == "__main__":
    ## Task 1
    # Generowanie grafu
    digraph_adjecency_matrix = generate_random_digraph_adjacency_matrix(8, 0.3)
    print("Macierz sąsiedztwa grafu skierowanego:")
    for row in digraph_adjecency_matrix:
        print(row)

    # Konwersja macierzy sąsiedztwa na graf skierowany
    digraph = convert_adjacency_matrix_to_digraph(digraph_adjecency_matrix)

    # Rysowanie grafu
    draw_circle_graph(digraph, 10, "circle_digraph.png")

    ## Task 2
    kosaraju_result = kosaraju(digraph_adjecency_matrix)
    print("Silnie spójne składowe grafu skierowanego:")
    for i, comp in enumerate(kosaraju_result):
        print(f"Wierzchołek {i} należy do składowej {comp}")

    draw_circle_graph(digraph, 10, "circle_digraph.png", colors=kosaraju_result)

    ## Task 3
    digraph_adjecency_matrix = add_weights_to_digraph(
        digraph_adjecency_matrix, min_weight=-5, max_weight=10
    )
    print("Macierz sąsiedztwa grafu skierowanego z wagami:")
    for row in digraph_adjecency_matrix:
        print(row)
    weighted_digraph = convert_adjacency_matrix_to_digraph(
        digraph_adjecency_matrix, weights=True
    )

    # Rysowanie grafu
    draw_circle_graph(weighted_digraph, 10, "circle_weighted_digraph.png", weights=True)

    test, bellman_ford_result = bellman_ford(digraph_adjecency_matrix, 0)
    print("Wynik algorytmu Bellmana-Forda:")
    print(f"Test: {test}")
    for i, dist in enumerate(bellman_ford_result):
        print(f"Najkrótsza odległość z wierzchołka 0 do wierzchołka {i} wynosi {dist}")

    ## Task 4
    johnson_result = johnson(digraph_adjecency_matrix)
    print("Wynik algorytmu Johnsona:")
    for i, row in enumerate(johnson_result):
        print(f"Najkrótsze odległości z wierzchołka {i}: {row}")
