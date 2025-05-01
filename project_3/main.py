from project_3.generator_connected import generate_weighted_connected_graph_nl
from project_1.draw_graph import draw_circle_graph
from project_1.converter import adjacency_matrix_to_graph
from project_3.algorithms import (
    dijkstra,
    kruskal,
    prim,
    graph_center,
    graph_center_minmax,
)

if __name__ == "__main__":

    # Zadanie 1: Generowanie ważonego, spójnego grafu o 8 wierzchołkach i 12 krawędziach
    graph_matrix = generate_weighted_connected_graph_nl(8, 12)

    # Konwersja macierzy sąsiedztwa na obiekt grafu do rysowania
    graph = adjacency_matrix_to_graph(graph_matrix)

    # Rysowanie grafu w układzie kołowym i zapis do pliku PNG z wagami krawędzi
    draw_circle_graph(graph, 5, "graph_project_3.png", weights=True)

    # Zadanie 2: Obliczenie najkrótszych ścieżek z wierzchołka 0 do pozostałych za pomocą algorytmu Dijkstry
    print("najkrótsza ścieżka z wierzchołka 0 do pozostałych wierzchołków:")
    print(dijkstra(graph_matrix, 0))

    # Zadanie 3: Obliczenie macierzy najkrótszych ścieżek między wszystkimi parami wierzchołków
    paths_matrix = [dijkstra(graph_matrix, node) for node in range(len(graph_matrix))]
    print("Macierz najkrótszych ścieżek:")
    for i in paths_matrix:
        print(
            i, sum(i), max(i)
        )  # wypisanie ścieżek z danego wierzchołka, ich sumy i maksymalnej wartości

    # Zadanie 4: Wyznaczenie centrum grafu (minimalna suma odległości) i centrum minmax (minimalna największa odległość)
    print("Centrum grafu:")
    print(
        graph_center(paths_matrix) + 1
    )  # +1 dla wypisania numeru wierzchołka zaczynając od 1, a nie od 0
    print("Centrum grafu minmax:")
    print(graph_center_minmax(paths_matrix) + 1)

    # Zadanie 5: Obliczenie minimalnego drzewa rozpinającego (MST) za pomocą algorytmów Kruskala i Prima
    mst_kruskal = kruskal(graph_matrix)
    mst_prim = prim(graph_matrix)

    # Rysowanie MST uzyskanego metodą Kruskala i zapis do pliku
    draw_circle_graph(
        adjacency_matrix_to_graph(mst_kruskal),
        5,
        "project_3_mst_kruskal.png",
        weights=True,
    )

    # Rysowanie MST uzyskanego metodą Prima i zapis do pliku
    draw_circle_graph(
        adjacency_matrix_to_graph(mst_prim),
        5,
        "project_3_mst_prim.png",
        weights=True,
    )
