# ======================
# BIBLIOTEKI
# ======================

import random  # losowość do generowania grafu
from collections import deque  # kolejka do BFS
import networkx as nx  # do wizualizacji grafu
import matplotlib.pyplot as plt
import matplotlib
import os
import math

matplotlib.use("Agg")  # Tryb bez interfejsu graficznego (do zapisu do pliku)


# ======================
# FUNKCJA RYSUJĄCA GRAF
# ======================

def draw_circle_graph(G, radius, name, directory=None, weights=False, colors="skyblue"):
    if not os.path.isdir("imgs"):
        os.mkdir("imgs")  # stwórz folder na obrazki, jeśli nie istnieje

    if directory is not None:
        path = os.path.join("imgs", directory)
        if not os.path.isdir(path):
            os.mkdir(path)

    # Rozmieszczenie wierzchołków na okręgu
    pos = {}
    n = len(G.nodes())
    for i, node in enumerate(G.nodes()):
        angle = 2 * math.pi / n
        pos[node] = (radius * math.cos(angle * i), radius * math.sin(angle * i))

    is_directed = isinstance(G, nx.DiGraph)

    nx.draw(
        G,
        pos,
        with_labels=True,
        node_color=colors,
        node_size=1500,
        font_size=12,
        font_weight="bold",
        arrows=is_directed,
        connectionstyle="arc3,rad=0.1",
    )

    if weights:
        # Dodaj etykiety z wagami krawędzi (np. przepustowości)
        edge_labels = {(u, v): G[u][v].get("weight", 1) for u, v in G.edges()}
        nx.draw_networkx_edge_labels(
            G,
            pos,
            edge_labels=edge_labels,
            font_size=10,
            font_color="red",
            label_pos=0.3,
            bbox=dict(facecolor="white", edgecolor="none", alpha=0.7),
        )

    # Zapis wykresu do pliku
    path = os.path.join("imgs", directory, name) if directory else os.path.join("imgs", name)
    plt.savefig(path)
    plt.clf()


# ======================
# ZADANIE 1 – Generowanie sieci przepływowej
# ======================

# Klasa reprezentująca graf przepływowy
class FlowNetwork:
    def __init__(self):
        self.graph = {}  # słownik sąsiedztwa: {u: {v: capacity}}
        self.nodes = set()

    def add_edge(self, u, v, capacity):
        self.nodes.add(u)
        self.nodes.add(v)
        if u not in self.graph:
            self.graph[u] = {}
        self.graph[u][v] = capacity  # krawędź skierowana z u do v o przepustowości

    def get_neighbors(self, u):
        return self.graph.get(u, {}).keys()

    def get_capacity(self, u, v):
        return self.graph[u].get(v, 0)

    def set_capacity(self, u, v, capacity):
        self.graph[u][v] = capacity

    def has_edge(self, u, v):
        return v in self.graph.get(u, {})

    def in_degree(self, v):
        # Liczba krawędzi kończących się w v
        return sum(1 for u in self.graph if v in self.graph[u])


# Funkcja do tworzenia warstwowego grafu
def generate_flow_network_no_libs(N):
    assert 2 <= N <= 4  # zabezpieczenie zgodnie z treścią zadania
    G = FlowNetwork()
    layers = [[] for _ in range(N + 2)]  # warstwy: 0 (źródło), ..., N+1 (ujście)

    node_counter = 0
    for i in range(N + 2):
        if i == 0 or i == N + 1:
            layers[i].append(f"v{node_counter}")  # źródło i ujście to po 1 wierzchołku
            node_counter += 1
        else:
            num_nodes = random.randint(2, N)
            for _ in range(num_nodes):
                layers[i].append(f"v{node_counter}")
                node_counter += 1

    # Tworzenie połączeń między warstwami
    for i in range(N + 1):
        for u in layers[i]:
            connected = False
            for _ in range(2 * len(layers[i + 1])):
                v = random.choice(layers[i + 1])
                if not G.has_edge(u, v):
                    G.add_edge(u, v, random.randint(1, 10))
                    connected = True
            if not connected:
                v = random.choice(layers[i + 1])
                G.add_edge(u, v, random.randint(1, 10))

        # Gwarantuj, że do każdego wierzchołka w warstwie i+1 ktoś prowadzi
        for v in layers[i + 1]:
            if G.in_degree(v) == 0:
                u = random.choice(layers[i])
                if not G.has_edge(u, v):
                    G.add_edge(u, v, random.randint(1, 10))

    # Dodaj 2N losowych dodatkowych krawędzi
    all_nodes = [n for layer in layers for n in layer]
    added = 0
    while added < 2 * N:
        u, v = random.sample(all_nodes, 2)
        if G.has_edge(u, v): continue
        if u in layers[-1] or v in layers[0]: continue  # nie wolno dodawać do źródła ani z ujścia
        G.add_edge(u, v, random.randint(1, 10))
        added += 1

    return G, layers


# ======================
# ZADANIE 2 – Ford-Fulkerson z BFS (Edmonds-Karp)
# ======================

def bfs(residual, source, sink, parent):
    visited = set()
    queue = deque([source])
    visited.add(source)

    while queue:
        u = queue.popleft()
        for v in residual.get_neighbors(u):
            if v not in visited and residual.get_capacity(u, v) > 0:
                visited.add(v)
                parent[v] = u
                if v == sink:
                    return True  # znaleziono ścieżkę powiększającą
                queue.append(v)
    return False  # brak ścieżki

def ford_fulkerson_no_libs(G, source, sink):
    residual = FlowNetwork()
    for u in G.graph:
        for v in G.graph[u]:
            residual.add_edge(u, v, G.graph[u][v])

    parent = {}
    max_flow = 0

    while bfs(residual, source, sink, parent):
        path_flow = float('inf')
        s = sink
        while s != source:
            u = parent[s]
            path_flow = min(path_flow, residual.get_capacity(u, s))
            s = parent[s]

        v = sink
        while v != source:
            u = parent[v]
            residual.set_capacity(u, v, residual.get_capacity(u, v) - path_flow)
            if residual.has_edge(v, u):
                residual.set_capacity(v, u, residual.get_capacity(v, u) + path_flow)
            else:
                residual.add_edge(v, u, path_flow)
            v = parent[v]

        max_flow += path_flow  # dodajemy przepływ ścieżki do całkowitego

    return max_flow


# ======================
# KONWERSJA do networkx do rysowania
# ======================

def convert_to_networkx(G):
    G_nx = nx.DiGraph()
    for u in G.graph:
        for v in G.graph[u]:
            G_nx.add_edge(u, v, weight=G.graph[u][v])
    return G_nx


# ======================
# URUCHOMIENIE PRZYKŁADOWEGO TESTU
# ======================

N = 3  # liczba warstw pośrednich
G, layers = generate_flow_network_no_libs(N)
source = layers[0][0]
sink = layers[-1][0]

G_nx = convert_to_networkx(G)
draw_circle_graph(G_nx, radius=10, name="sieć_przepływowa.png", weights=True)

print("ZADANIE 1: Wygenerowany graf:")
for u in G.graph:
    for v in G.graph[u]:
        print(f"{u} -> {v} | capacity = {G.graph[u][v]}")

max_flow = ford_fulkerson_no_libs(G, source, sink)
print(f"\nZADANIE 2: Maksymalny przepływ z {source} do {sink}: {max_flow}")
