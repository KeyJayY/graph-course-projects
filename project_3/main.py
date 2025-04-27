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

    # task 1
    graph_matrix = generate_weighted_connected_graph_nl(8, 12)
    graph = adjacency_matrix_to_graph(graph_matrix)
    draw_circle_graph(graph, 5, "graph_project_3.png", weights=True)

    # task 2
    print("najkrótsza ścieżka z wierzchołka 0 do pozostałych wierzchołków:")
    print(dijkstra(graph_matrix, 0))

    # task 3
    paths_matrix = [dijkstra(graph_matrix, node) for node in range(len(graph_matrix))]
    print("Macierz najkrótszych ścieżek:")
    for i in paths_matrix:
        print(i)

    # task 4
    print("Centrum grafu:")
    print(graph_center(paths_matrix))
    print("Centrum grafu minmax:")
    print(graph_center_minmax(paths_matrix))

    # task 5
    mst_kruskal = kruskal(graph_matrix)
    mst_prim = prim(graph_matrix)

    draw_circle_graph(
        adjacency_matrix_to_graph(mst_kruskal),
        5,
        "project_3_mst_kruskal.png",
        weights=True,
    )

    draw_circle_graph(
        adjacency_matrix_to_graph(mst_prim),
        5,
        "project_3_mst_prim.png",
        weights=True,
    )
