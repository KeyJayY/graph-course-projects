def dijkstra(graph_matrix, start):
    """Implementacja algorytmu Dijkstry na podstawie macierzy sąsiedztwa."""
    n = len(graph_matrix)
    visited = set()
    distances = [float("inf")] * n
    distances[start] = 0

    while len(visited) < n:
        current = min(
            (node for node in range(n) if node not in visited),
            key=lambda node: distances[node],
        )
        visited.add(current)

        for neighbor, weight in enumerate(graph_matrix[current]):
            if weight > 0 and neighbor not in visited:
                distances[neighbor] = min(
                    distances[neighbor], distances[current] + weight
                )

    return distances


def convert_adjecency_matrix_to_edges_list(graph_matrix):
    """Konwertuje macierz sąsiedztwa na listę krawędzi."""
    edges = []
    n = len(graph_matrix)

    for i in range(n):
        for j in range(i + 1, n):
            if graph_matrix[i][j] != 0:
                edges.append((i, j, graph_matrix[i][j]))
    return edges


def convert_edges_list_to_adjecency_matrix(edges_list, n):
    """Konwertuje listę krawędzi na macierz sąsiedztwa."""
    graph_matrix = [[0] * n for _ in range(n)]
    for i, j, weight in edges_list:
        graph_matrix[i][j] = graph_matrix[j][i] = weight
    return graph_matrix


def kruskal(graph_matrix):
    """ "Implementacja algorytmu Kruskala na podstawie macierzy sąsiedztwa."""
    sets = [{node} for node in range(len(graph_matrix))]
    edges = convert_adjecency_matrix_to_edges_list(graph_matrix)
    edges.sort(key=lambda edge: edge[2])
    mst = []

    for i, j, weight in edges:
        set_i = next((s for s in sets if i in s), None)
        set_j = next((s for s in sets if j in s), None)

        if set_i != set_j:
            mst.append((i, j, weight))
            sets.remove(set_i)
            sets.remove(set_j)
            sets.append(set_i.union(set_j))

    return convert_edges_list_to_adjecency_matrix(mst, len(graph_matrix))


def prim(graph_matrix):
    """Implementacja algorytmu Prima na podstawie macierzy sąsiedztwa."""
    n = len(graph_matrix)
    in_mst = [False] * n
    key = [float("inf")] * n
    parent = [-1] * n
    key[0] = 0

    for _ in range(n):
        u = min((i for i in range(n) if not in_mst[i]), key=lambda i: key[i])
        in_mst[u] = True

        for v in range(n):
            if 0 < graph_matrix[u][v] < key[v] and not in_mst[v]:
                key[v] = graph_matrix[u][v]
                parent[v] = u

    mst_edges = [
        (parent[v], v, graph_matrix[parent[v]][v])
        for v in range(1, n)
        if parent[v] != -1
    ]

    return convert_edges_list_to_adjecency_matrix(mst_edges, n)


def graph_center(paths_matrix):
    """Zwraca wierzchołek centrum grafu."""
    return min(range(len(paths_matrix)), key=lambda node: sum(paths_matrix[node]))


def graph_center_minmax(paths_matrix):
    """Zwraca wierzchołek centrum grafu minmax."""
    return min(range(len(paths_matrix)), key=lambda node: max(paths_matrix[node]))
