import networkx as nx
from project_1.draw_graph import draw_circle_graph


def hamiltonian_cycle_util(G, path, visited, start):
    """
    Rekurencyjna funkcja pomocnicza do znalezienia cyklu Hamiltona.
    Sprawdza, czy istnieje cykl Hamiltona w grafie, odwiedzając każdy wierzchołek dokładnie raz,
    a potem wraca do wierzchołka początkowego.

    :param G: graf, w którym szukamy cyklu Hamiltona
    :param path: aktualna ścieżka, którą odwiedziliśmy wierzchołki
    :param visited: słownik, który śledzi, które wierzchołki zostały odwiedzone
    :param start: wierzchołek początkowy cyklu
    :return: cykl Hamiltona (lista wierzchołków) lub None, jeśli cykl nie istnieje
    """
    if len(path) == len(G):
        if start in G.neighbors(path[-1]):
            return path + [start]
        else:
            return None

    for neighbor in G.neighbors(path[-1]):
        if not visited[neighbor]:
            visited[neighbor] = True
            result = hamiltonian_cycle_util(G, path + [neighbor], visited, start)
            if result:
                return result
            visited[neighbor] = False
    return None


def find_hamiltonian_cycle(G):
    """
    Funkcja do znalezienia cyklu Hamiltona w grafie.
    Używa funkcji rekurencyjnej `hamiltonian_cycle_util` do próby utworzenia cyklu.

    :param G: graf, w którym szukamy cyklu Hamiltona
    :return: cykl Hamiltona (lista wierzchołków) lub None, jeśli cykl nie istnieje
    """
    visited = {node: False for node in G.nodes}

    for start in G.nodes:
        visited[start] = True
        path = [start]
        cycle = hamiltonian_cycle_util(G, path, visited, start)
        if cycle:
            return cycle
        visited[start] = False

    return None


def main():
    """
    Główna funkcja programu, która generuje graf, rysuje go, a następnie znajduje cykl Hamiltona.
    """
    G = nx.Graph()

    edges = [(0, 1), (1, 2), (2, 3), (3, 0), (0, 2)]
    G.add_edges_from(edges)

    draw_circle_graph(G, radius=10, name="hamiltonian_graph.png", weights=False)

    cycle = find_hamiltonian_cycle(G)
    if cycle:
        print("Graf jest hamiltonowski.")
        print("Cykl Hamiltona:", cycle)
    else:
        print("Graf NIE jest hamiltonowski.")


if __name__ == "__main__":
    main()
