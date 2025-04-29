import networkx as nx
from project_1.draw_graph import draw_circle_graph

def havel_hakimi(sequence):
    """
    Sprawdza, czy podany ciąg liczb jest ciągiem graficznym
    (czyli czy da się z niego skonstruować graf prosty).
    Wersja algorytmu Havel-Hakimi.
    """
    seq = sequence[:]
    while True:
        seq.sort(reverse=True)

        if all(d == 0 for d in seq):
            return True

        d = seq.pop(0)

        if d > len(seq):
            return False

        for i in range(d):
            seq[i] -= 1
            if seq[i] < 0:
                return False


def build_graph(sequence):
    """
    Tworzy graf na podstawie ciągu graficznego.
    Wierzchołki mają stopnie zgodne z podanym ciągiem.
    """
    G = nx.Graph()
    seq = sorted([(deg, i) for i, deg in enumerate(sequence)], reverse=True)

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

def main():
    """
    Główna funkcja programu – sprawdza czy ciąg jest graficzny,
    buduje graf i zapisuje jego wizualizację.
    """
    ciag = [4, 2, 4, 2, 1, 1]

    if havel_hakimi(ciag):
        print("Ciąg jest graficzny.")
        graf = build_graph(ciag)
        draw_circle_graph(graf, radius=10, name="generated_graph.png", weights=False)
    else:
        print("Ciąg NIE jest graficzny.")

if __name__ == "__main__":
    main()
