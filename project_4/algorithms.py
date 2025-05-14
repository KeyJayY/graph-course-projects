import math
import heapq
from typing import List, Tuple, Optional

# Algorytm Kosaraju do znajdowania silnie spójnych składowych grafu skierowanego


def kosaraju(adj: List[List[int]]) -> List[int]:
    """
    Znajduje silnie spójne składowe grafu skierowanego.
    adj: macierz sąsiedztwa, gdzie adj[u][v] != 0 oznacza krawędź z u do v.
    Zwraca listę comp, gdzie comp[v] to numer składowej (liczone od 1).
    """
    n = len(adj)
    visited = [False] * n
    stack = []

    def dfs1(u: int):
        visited[u] = True
        for v in range(n):
            if adj[u][v] != 0 and not visited[v]:
                dfs1(v)
        stack.append(u)

    # Pierwsze przejście: porządek kończenia przeszukiwania
    for u in range(n):
        if not visited[u]:
            dfs1(u)

    # Transpozycja grafu
    adj_T = [[0] * n for _ in range(n)]
    for u in range(n):
        for v in range(n):
            if adj[u][v] != 0:
                adj_T[v][u] = adj[u][v]

    # Drugie przejście: przypisanie składowych
    comp = [0] * n
    current_comp = 0

    def dfs2(u: int):
        comp[u] = current_comp
        for v in range(n):
            if adj_T[u][v] != 0 and comp[v] == 0:
                dfs2(v)

    while stack:
        u = stack.pop()
        if comp[u] == 0:
            current_comp += 1
            dfs2(u)

    return comp


# Algorytm Bellmana-Forda do znajdowania najkrótszych ścieżek z jednego źródła
def bellman_ford(w: List[List[Optional[float]]], s: int) -> Tuple[bool, List[float]]:
    """
    Oblicza najkrótsze ścieżki z wierzchołka s w grafie skierowanym z wagami.
    w[u][v] = waga krawędzi z u do v lub math.inf/None jeśli brak krawędzi.
    Zwraca (brak_ujemnego_cyklu, lista_odległości).
    Jeśli istnieje cykl o ujemnej wadze dostępny z s, zwraca (False, odległości).
    """
    n = len(w)
    dist = [math.inf] * n
    dist[s] = 0

    # Relaksacja krawędzi n-1 razy
    for _ in range(n - 1):
        updated = False
        for u in range(n):
            for v in range(n):
                weight = w[u][v]
                if weight is not None and weight != math.inf:
                    if dist[u] + weight < dist[v]:
                        dist[v] = dist[u] + weight
                        updated = True
        if not updated:
            break

    # Sprawdzenie cykli ujemnych
    for u in range(n):
        for v in range(n):
            weight = w[u][v]
            if weight is not None and weight != math.inf:
                if dist[u] + weight < dist[v]:
                    return False, dist
    return True, dist


# Algorytm Dijkstry dla grafów o nieujemnych wagach


def dijkstra(w: List[List[Optional[float]]], src: int) -> List[float]:
    """
    Oblicza najkrótsze ścieżki z wierzchołka src w grafie z nieujemnymi wagami.
    w[u][v] = waga lub math.inf/None jeśli brak krawędzi.
    Zwraca listę odległości.
    """
    n = len(w)
    dist = [math.inf] * n
    dist[src] = 0
    pq = [(0, src)]  # (odległość, wierzchołek)

    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        for v in range(n):
            weight = w[u][v]
            if weight is not None and weight != math.inf:
                nd = d + weight
                if nd < dist[v]:
                    dist[v] = nd
                    heapq.heappush(pq, (nd, v))
    return dist


# Algorytm Johnsona do wyznaczania najkrótszych ścieżek między wszystkimi parami wierzchołków


def johnson(w: List[List[Optional[float]]]) -> List[List[float]]:
    """
    Oblicza najkrótsze ścieżki między wszystkimi parami wierzchołków przy pomocy algorytmu Johnsona.
    w[u][v] = waga krawędzi lub None/math.inf jeśli brak krawędzi.
    Zwraca macierz D: n x n z odległościami.
    Rzuca wyjątek jeśli istnieje cykl o ujemnej wadze.
    """
    n = len(w)
    # Tworzenie G' z dodatkowym wierzchołkiem s = n
    w_prime = [row[:] + [math.inf] for row in w]
    w_prime.append([math.inf] * (n + 1))
    for v in range(n):
        w_prime[n][v] = 0

    # Bellman-Ford dla G'
    has_no_cycle, h = bellman_ford(w_prime, n)
    if not has_no_cycle:
        raise ValueError("Graf zawiera cykl o ujemnej wadze")

    # Przeskalowanie wag: w_hat[u][v] = w[u][v] + h[u] - h[v]
    w_hat = [[None] * n for _ in range(n)]
    for u in range(n):
        for v in range(n):
            weight = w[u][v]
            if weight is not None and weight != math.inf:
                w_hat[u][v] = weight + h[u] - h[v]
            else:
                w_hat[u][v] = None

    # Obliczenie D[u][v]
    D = [[math.inf] * n for _ in range(n)]
    for u in range(n):
        d_hat = dijkstra(w_hat, u)
        for v in range(n):
            if d_hat[v] < math.inf:
                D[u][v] = d_hat[v] - h[u] + h[v]
    return D
