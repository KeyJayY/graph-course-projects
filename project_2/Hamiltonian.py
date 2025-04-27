import networkx as nx
import matplotlib.pyplot as plt

def hamiltonian_cycle_util(G, path, visited, start):
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
    n = len(G.nodes)
    visited = {node: False for node in G.nodes}

    for start in G.nodes:
        visited[start] = True
        path = [start]
        cycle = hamiltonian_cycle_util(G, path, visited, start)
        if cycle:
            return cycle
        visited[start] = False

    return None

def visualize_graph(G):
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=800, font_size=12)
    plt.title("Graf do sprawdzenia cyklu Hamiltona")
    plt.show()

if __name__ == '__main__':
    G = nx.Graph()
    edges = [(0, 1), (1, 2), (2, 3), (3, 0), (0, 2)]
    G.add_edges_from(edges)

    visualize_graph(G)

    cycle = find_hamiltonian_cycle(G)
    if cycle:
        print("Graf jest hamiltonowski.")
        print("Cykl Hamiltona:", cycle)
    else:
        print("Graf NIE jest hamiltonowski.")
