import random  # Do losowania liczby wierzchołków i przepustowości
from collections import deque  # Do implementacji kolejki w BFS
import networkx as nx  # Do rysowania grafów
import matplotlib.pyplot as plt  # Do tworzenia wykresów
import matplotlib
import os  # Do tworzenia folderów
import math  # Do rozmieszczania wierzchołków na okręgu

# Ustawienie backendu, który pozwala zapisywać wykresy do plików
matplotlib.use("Agg")

# ============================
# RYSOWANIE GRAFU W UKŁADZIE KOŁOWYM
# ============================
def draw_circle_graph(G, radius, name, directory=None, weights=False, colors="skyblue"):
    if not os.path.isdir("imgs"):
        os.mkdir("imgs")

    if directory is not None:
        path = os.path.join("imgs", directory)
        if not os.path.isdir(path):
            os.mkdir(path)

    pos = {}
    n = len(G.nodes())  # Liczba wierzchołków
    for i, node in enumerate(G.nodes()):
        angle = 2 * math.pi / n
        pos[node] = (radius * math.cos(angle * i), radius * math.sin(angle * i))

    is_directed = isinstance(G, nx.DiGraph)  # Sprawdzenie, czy graf jest skierowany

    # Rysowanie wierzchołków i krawędzi
    nx.draw(
        G, pos,
        with_labels=True,
        node_color=colors,
        node_size=1500,
        font_size=12,
        font_weight="bold",
        arrows=is_directed,
        connectionstyle="arc3,rad=0.1",
    )

    if weights:
        # Etykiety z wagami krawędzi (czyli przepustowościami)
        edge_labels = {(u, v): G[u][v].get("weight", 1) for u, v in G.edges()}
        nx.draw_networkx_edge_labels(
            G, pos,
            edge_labels=edge_labels,
            font_size=10,
            font_color="red",
            label_pos=0.3,
            bbox=dict(facecolor="white", edgecolor="none", alpha=0.7),
        )

    # Zapis wykresu do pliku PNG
    save_path = os.path.join("imgs", directory, name) if directory else os.path.join("imgs", name)
    plt.savefig(save_path)
    plt.clf()

# ============================
# KLASA REPREZENTUJĄCA GRAF PRZEPŁYWOWY
# ============================
class FlowNetwork:
    def __init__(self):
        self.graph = {}  # Słownik: wierzchołek -> {sąsiad: przepustowość}
        self.nodes = set()  # Zbór wszystkich wierzchołków

    def add_edge(self, u, v, capacity):
        self.nodes.add(u)
        self.nodes.add(v)
        if u not in self.graph:
            self.graph[u] = {}
        self.graph[u][v] = capacity  # Dodaje krawędź skierowaną z u do v z daną przepustowością

    def get_neighbors(self, u):
        return self.graph.get(u, {}).keys()  # Zwraca sąsiadów danego wierzchołka

    def get_capacity(self, u, v):
        return self.graph[u].get(v, 0)  # Zwraca przepustowość krawędzi (0 jeśli nie istnieje)

    def set_capacity(self, u, v, capacity):
        self.graph[u][v] = capacity  # Ustawia nową przepustowość

    def has_edge(self, u, v):
        return v in self.graph.get(u, {})  # Sprawdza, czy istnieje krawędź

    def in_degree(self, v):
        return sum(1 for u in self.graph if v in self.graph[u])  # Liczy ilu ma poprzedników

# ============================
# GENEROWANIE LOSOWEJ SIECI PRZEPŁYWOWEJ
# ============================
def generate_flow_network(N):
    assert 2 <= N <= 4  # Liczba warstw pośrednich musi być od 2 do 4
    G = FlowNetwork()
    layers = [[] for _ in range(N + 2)]  # Warstwy: 0 - źródło, N+1 - ujście

    node_id = 0  # Unikalny numer wierzchołka
    for i in range(N + 2):
        if i == 0 or i == N + 1:
            layers[i].append(f"v{node_id}")
            node_id += 1
        else:
            for _ in range(random.randint(2, N)):
                layers[i].append(f"v{node_id}")
                node_id += 1

    # Łączenie warstw kolejno: warstwa i -> warstwa i+1
    for i in range(N + 1):
        for u in layers[i]:
            has_out = False
            for _ in range(2 * len(layers[i + 1])):
                v = random.choice(layers[i + 1])
                if not G.has_edge(u, v):
                    G.add_edge(u, v, random.randint(1, 10))
                    has_out = True
            if not has_out:
                v = random.choice(layers[i + 1])
                G.add_edge(u, v, random.randint(1, 10))

        # Upewnij się, że każdy wierzchołek w i+1 ma co najmniej jedno wejście
        for v in layers[i + 1]:
            if G.in_degree(v) == 0:
                u = random.choice(layers[i])
                if not G.has_edge(u, v):
                    G.add_edge(u, v, random.randint(1, 10))

    # Dodajemy 2N losowych krawędzi spoza struktury warstw
    all_nodes = [n for layer in layers for n in layer]
    added = 0
    
    while added < 2 * N:
        u, v = random.sample(all_nodes, 2)
        if u in layers[-1] or v in layers[0]: # Nie dodawaj krawędzi do źródła ani z ujścia
            continue
        if G.has_edge(u, v) or G.has_edge(v, u):  # UWZGLĘDNIONE OBA KIERUNKI
            continue
        G.add_edge(u, v, random.randint(1, 10))
        added += 1


    return G, layers


# ============================
# ALGORYTM BFS DO ZNAJDOWANIA ŚCIEŻEK POWIĘKSZAJĄCYCH
# ============================
def bfs(residual, source, sink, parent):
    visited = set()  # Zbiór odwiedzonych wierzchołków
    queue = deque([source])  # Kolejka do BFS
    visited.add(source)

    while queue:
        u = queue.popleft()  # Pobieramy pierwszy element z kolejki
        for v in residual.get_neighbors(u):  # Iterujemy po sąsiadach
            if v not in visited and residual.get_capacity(u, v) > 0:
                visited.add(v)
                parent[v] = u  # Zapamiętujemy ścieżkę
                if v == sink:
                    return True  # Znaleziono ścieżkę do ujścia
                queue.append(v)  # Dodajemy do kolejki
    return False  # Nie znaleziono ścieżki powiększającej

# ============================
# ALGORYTM FORDA-FULKERSONA Z BFS (EDMONDS-KARP)
# ============================
def ford_fulkerson(G, source, sink):
    residual = FlowNetwork()  # Tworzymy graf rezydualny (resztkowy)
    for u in G.graph:
        for v in G.graph[u]:
            residual.add_edge(u, v, G.graph[u][v])  # Kopiujemy przepustowości

    max_flow = 0  # Początkowy przepływ = 0
    parent = {}  # Ścieżka
    path_count = 1  # Licznik ścieżek

    while bfs(residual, source, sink, parent):
        path_flow = float('inf')
        v = sink
        path = [v]  # Zbieramy wierzchołki na ścieżce
        while v != source:
            u = parent[v]
            path_flow = min(path_flow, residual.get_capacity(u, v))  # Znajdujemy minimum na ścieżce
            v = u
            path.append(v)

        path.reverse()  # Ścieżka od źródła do ujścia
        print(f"Ścieżka {path_count}: {' -> '.join(path)} | przepływ = {path_flow}")
        path_count += 1

        # Aktualizujemy przepustowości w grafie resztkowym
        v = sink
        while v != source:
            u = parent[v]
            residual.set_capacity(u, v, residual.get_capacity(u, v) - path_flow)
            if residual.has_edge(v, u):
                residual.set_capacity(v, u, residual.get_capacity(v, u) + path_flow)
            else:
                residual.add_edge(v, u, path_flow)
            v = u

        max_flow += path_flow  # Dodajemy przepływ tej ścieżki do całkowitego

    return max_flow

# ============================
# KONWERSJA GRAFU DO NETWORKX W CELU WIZUALIZACJI
# ============================
def convert_to_networkx(G):
    G_nx = nx.DiGraph()
    for u in G.graph:
        for v in G.graph[u]:
            G_nx.add_edge(u, v, weight=G.graph[u][v])  # Tworzymy krawędź z wagą (przepustowością)
    return G_nx

# ============================
# BLOK GŁÓWNY
# ============================
N = 3  # Liczba warstw pośrednich
G, layers = generate_flow_network(N)  # Generujemy sieć
source = layers[0][0]  # Źródło to pierwszy wierzchołek warstwy 0
sink = layers[-1][0]  # Ujście to pierwszy wierzchołek ostatniej warstwy

G_nx = convert_to_networkx(G)  # Konwersja do networkx do rysowania

draw_circle_graph(G_nx, radius=10, name="sieć_z5.png", weights=True)  # Rysowanie i zapis grafu

# Wypisanie krawędzi i przepustowości
print("ZADANIE 1: Graf przepływowy (wierzchołki i krawędzie):")
for u in G.graph:
    for v in G.graph[u]:
        print(f"{u} -> {v} | capacity = {G.graph[u][v]}")

# Obliczenie maksymalnego przepływu i wypisanie ścieżek
print("\nZADANIE 2: Ścieżki powiększające:")
max_flow = ford_fulkerson(G, source, sink)
print(f"\nMaksymalny przepływ z {source} do {sink} wynosi: {max_flow}")
