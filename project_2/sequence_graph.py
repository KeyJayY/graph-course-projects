import networkx as nx
from project_1.draw_graph import draw_circle_graph

def havel_hakimi(sequence):
    seq = sequence[:]
    while True:
        seq = sorted([d for d in seq if d > 0], reverse=True)
        if not seq:
            return True
        d = seq.pop(0)
        if d > len(seq):
            return False
        for i in range(d):
            seq[i] -= 1
            if seq[i] < 0:
                return False

def build_graph(sequence):
    G = nx.Graph()
    seq = sorted([(deg, i) for i, deg in enumerate(sequence)], reverse=True)
    n = len(sequence)

    while seq:
        seq.sort(reverse=True)
        d, v = seq.pop(0)
        if d > len(seq):
            raise ValueError("Nieprawidłowy ciąg graficzny")

        for i in range(d):
            deg_i, u = seq[i]
            seq[i] = (deg_i - 1, u)
            G.add_edge(v, u)

        if any(deg < 0 for deg, _ in seq):
            raise ValueError("Nieprawidłowy ciąg graficzny")

    return G



if __name__ == "__main__":
    ciag = [4, 2, 4, 2, 1, 1]

    if havel_hakimi(ciag):
        print("Ciąg jest graficzny.")
        graf = build_graph(ciag)
        draw_circle_graph(G, radius=10, name="generated_graph.png", weights=False)
        print("Ciąg NIE jest graficzny.")
