import networkx as nx
from collections import defaultdict
from project_1.draw_graph import draw_circle_graph


def components_R(nr, i, G, connected_graph_list):
    """
    Rekurencyjna funkcja do oznaczania wierzchołków należących do tej samej składowej spójności.
    Przechodzi po sąsiadach wierzchołka i oznacza je numerem komponentu spójności.

    :param nr: numer komponentu spójności, który jest przypisany do wierzchołka
    :param i: aktualnie odwiedzany wierzchołek
    :param G: graf, w którym szukamy komponentów spójności
    :param connected_graph_list: lista, w której przechowywane są numery komponentów spójności dla każdego wierzchołka
    """
    for j in G.neighbors(i):
        if connected_graph_list[j] == -1:
            connected_graph_list[j] = nr
            components_R(nr, j, G, connected_graph_list)


def connected_components_R(G):
    """
    Funkcja do wyznaczania komponentów spójności w grafie.
    Dla każdego wierzchołka przypisuje numer komponentu spójności, do którego należy.

    :param G: graf, w którym szukamy komponentów spójności
    :return: lista, w której dla każdego wierzchołka zapisany jest numer komponentu spójności
    """
    connected_graph_list = [-1 for _ in range(G.number_of_nodes())]
    nr = 0

    for i in range(G.number_of_nodes()):
        if connected_graph_list[i] == -1:
            nr += 1
            connected_graph_list[i] = nr
            components_R(nr, i, G, connected_graph_list)

    return connected_graph_list


def print_components(connected_graph_list):
    """
    Funkcja do wypisania wszystkich komponentów spójności w grafie.
    Grupuje wierzchołki według komponentu spójności i wypisuje je w formie listy.

    :param connected_graph_list: lista numerów komponentów spójności dla każdego wierzchołka
    """
    components = defaultdict(list)

    for vertex, component_num in enumerate(connected_graph_list):
        components[component_num].append(vertex)

    print("Składowe spójności:")
    for comp_num in sorted(components.keys()):
        vertices = " ".join(map(str, components[comp_num]))
        print(f"{comp_num}) {vertices}")

    # Określamy numer największej składowej
    largest_component = max(components.items(), key=lambda x: len(x[1]))[0]
    print(f"Największa składowa ma numer {largest_component}.")


def main():
    """
    Główna funkcja programu, która generuje graf, wyznacza komponenty spójności,
    wypisuje je i rysuje graf.
    """
    G = nx.Graph()

    G.add_edges_from([(0, 1), (1, 2)])
    G.add_edges_from([(3, 4), (4, 5), (5, 3), (5, 6)])

    connected_graph_list = connected_components_R(G)
    print_components(connected_graph_list)
    draw_circle_graph(G, radius=10, name="components_graph.png", weights=False)


if __name__ == "__main__":
    main()
