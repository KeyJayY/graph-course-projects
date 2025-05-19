import random
import numpy as np
from collections import defaultdict
import time # Opcjonalnie do mierzenia czasu wykonania

# --- Konfiguracja i dane wejściowe ---

# Przykład digrafu w postaci słownika {wierzchołek: [sąsiedzi_wyjściowi]}
# Możemy mieć wierzchołki występujące tylko jako sąsiedzi,
# dlatego musimy zebrać wszystkie unikalne wierzchołki.
example_graph = {
    'A': ['B', 'C'],
    'B': ['C'],
    'C': ['A'],
    'D': ['A'], # Wierzchołek D ma tylko wychodzącą krawędź do A
    'E': []     # Wierzchołek E to "wiszący" wierzchołek (dead end)
}

# Zbierz wszystkie unikalne wierzchołki z kluczy i wartości (sąsiadów)
all_nodes = sorted(list(set(example_graph.keys()).union(
    set(node for neighbors in example_graph.values() for node in neighbors)
)))
print(f"Wszystkie wierzchołki w grafie: {all_nodes}")
n = len(all_nodes)
print(f"Liczba wierzchołków (n): {n}")

# Parametr tłumienia (damping factor) - prawdopodobieństwo teleportacji
d = 0.15

# --- Metoda (a): Błądzenie przypadkowe z teleportacją ---

def pagerank_random_walk(graph, nodes, d, steps=100000):
    """
    Oblicza PageRank przy użyciu symulacji błądzenia przypadkowego z teleportacją.

    Args:
        graph (dict): Digraf w formacie {wierzchołek: [sąsiedzi]}.
        nodes (list): Lista wszystkich unikalnych wierzchołków.
        d (float): Współczynnik tłumienia (prawdopodobieństwo teleportacji).
        steps (int): Liczba kroków symulacji.

    Returns:
        dict: Słownik {wierzchołek: pagerank_score}.
    """
    n = len(nodes)
    # Inicjalizacja liczników odwiedzin dla wszystkich wierzchołków
    visits = {node: 0 for node in nodes}

    # Początkowy wierzchołek - wybieramy losowo spośród wszystkich wierzchołków
    current_node = random.choice(nodes)

    print(f"\n--- Metoda (a): Błądzenie przypadkowe ({steps} kroków) ---")
    print(f"Start symulacji z wierzchołka: {current_node}")
    start_time = time.time()

    for step in range(steps):
        visits[current_node] += 1

        # Losowanie z prawdopodobieństwem d
        # Jeśli wylosowana liczba jest mniejsza niż d, teleportujemy
        if random.random() < d:
            # Teleportacja do losowego wierzchołka ze wszystkich wierzchołków
            next_node = random.choice(nodes)
        else:
            # Przejście po krawędzi (jeśli istnieją sąsiedzi)
            neighbors = graph.get(current_node, [])
            if not neighbors:
                # Jeśli wierzchołek jest 'dead end' (nie ma wychodzących krawędzi)
                # zgodnie z definicją błądzenia przypadkowego, surfer teleportuje.
                # W praktyce jest to równoważne teleportacji z prob. 1.
                # Nasza struktura 'else' już to obsłuży, jeśli potraktujemy to
                # jako przypadek, gdzie 'random.random() >= d' ale nie można
                # wykonać kroku po krawędzi. Standardowe podejście to *zawsze*
                # teleportować z dead end. Zmodyfikujmy to dla jasności:
                 next_node = random.choice(nodes) # Z dead end zawsze teleportacja
            else:
                # Losowe przejście do sąsiada
                next_node = random.choice(neighbors)

        current_node = next_node

    end_time = time.time()
    print(f"Symulacja zakończona w {end_time - start_time:.4f} sekundy.")

    # Obliczenie częstości odwiedzin
    total_visits = sum(visits.values())
    # Zapobiegamy dzieleniu przez zero, gdyby steps było 0 (choć mało prawdopodobne)
    pagerank_scores = {node: count / total_visits if total_visits > 0 else 0 for node, count in visits.items()}

    return pagerank_scores

# --- Metoda (b): Iteracja wektora obsadzeń ---

def pagerank_power_iteration(graph, nodes, d, iterations=200, tolerance=1e-7):
    """
    Oblicza PageRank przy użyciu metody iteracji wektora obsadzeń.

    Args:
        graph (dict): Digraf w formacie {wierzchołek: [sąsiedzi]}.
        nodes (list): Lista wszystkich unikalnych wierzchołków.
        d (float): Współczynnik tłumienia (prawdopodobieństwo teleportacji).
        iterations (int): Maksymalna liczba iteracji.
        tolerance (float): Próg zbieżności (norma L1 różnicy wektorów).

    Returns:
        dict: Słownik {wierzchołek: pagerank_score}.
    """
    n = len(nodes)

    # Mapowanie wierzchołków na indeksy dla operacji macierzowych
    node_to_index = {node: i for i, node in enumerate(nodes)}
    index_to_node = {i: node for i, node in enumerate(nodes)}

    # Obliczanie stopni wyjściowych dla wszystkich wierzchołków
    out_degrees = {node: len(graph.get(node, [])) for node in nodes}

    # Konstruowanie macierzy M' (ze zmodyfikowanymi wierszami dla dead ends)
    # M'[i, j] = 1/out_degree(i) jeśli istnieje krawędź i->j i out_degree(i)>0
    # M'[i, j] = 1/n jeśli out_degree(i) == 0
    M_prime = np.zeros((n, n))
    for i, node_i in enumerate(nodes):
        degree_i = out_degrees[node_i]
        if degree_i == 0:
            # Wierzchołek wiszący - równe prawdopodobieństwo przejścia do każdego wierzchołka
            M_prime[i, :] = 1.0 / n
        else:
            # Normalne przejście po krawędziach wychodzących
            neighbors = graph.get(node_i, [])
            for neighbor_node in neighbors:
                j = node_to_index[neighbor_node]
                M_prime[i, j] = 1.0 / degree_i

    # Konstruowanie macierzy przejścia PageRank P
    # P = (1-d) * M' + d * J/n (gdzie J to macierz jedynek)
    teleport_matrix = np.full((n, n), 1.0 / n)
    P = (1 - d) * M_prime + d * teleport_matrix

    # Inicjalizacja wektora PageRank (jednostajny rozkład prawdopodobieństwa)
    # p to wektor wierszowy [1/n, 1/n, ..., 1/n]
    p = np.full(n, 1.0 / n)

    print("\n--- Metoda (b): Iteracja wektora obsadzeń ---")
    start_time = time.time()

    # Iteracje potęgowe
    for i in range(iterations):
        # Obliczenie nowego wektora obsadzeń: p_next = p_current * P
        p_next = p @ P

        # Sprawdzenie zbieżności przy użyciu normy L1
        # Różnica między nowym a poprzednim wektorem jest mała
        if np.linalg.norm(p_next - p, ord=1) < tolerance:
            end_time = time.time()
            print(f"Zbieżność osiągnięta po {i+1} iteracjach w {end_time - start_time:.4f} sekundy.")
            p = p_next # Aktualizujemy p do zbieżnego wektora
            break
        p = p_next # Aktualizujemy wektor do następnej iteracji
    else:
        # Wykonuje się, jeśli pętla zakończyła się przez wyczerpanie iteracji
        end_time = time.time()
        print(f"Nie osiągnięto zbieżności po {iterations} iteracjach w {end_time - start_time:.4f} sekundy.")


    # Wektor p po zbieżności (lub maksymalnej liczbie iteracji) zawiera wartości PageRank
    # Możliwa drobna renormalizacja z powodu błędów numerycznych, choć dla P stochastycznej suma powinna być ~1
    # p /= p.sum() # Zazwyczaj niepotrzebne przy poprawnej implementacji i zbieżności

    # Przekształcenie wektora NumPy na słownik {wierzchołek: score}
    pagerank_scores = {index_to_node[i]: score for i, score in enumerate(p)}

    return pagerank_scores

# --- Wykonanie i porównanie ---

# Uruchomienie metody (a)
# Zalecana duża liczba kroków dla lepszej dokładności
pagerank_a = pagerank_random_walk(example_graph, all_nodes, d, steps=200000)

print("\nWyniki PageRank (Metoda a - symulacja błądzenia przypadkowego):")
# Sortowanie wyników według nazw wierzchołków dla łatwiejszego porównania
sorted_pagerank_a = dict(sorted(pagerank_a.items()))
for node, score in sorted_pagerank_a.items():
    print(f"  {node}: {score:.8f}") # Drukujemy więcej miejsc po przecinku dla porównania
print("-" * 40)

# Uruchomienie metody (b)
# Zalecana odpowiednia liczba iteracji lub próg zbieżności
pagerank_b = pagerank_power_iteration(example_graph, all_nodes, d, iterations=200, tolerance=1e-8)

print("\nWyniki PageRank (Metoda b - iteracja wektora obsadzeń):")
# Sortowanie wyników według nazw wierzchołków dla łatwiejszego porównania
sorted_pagerank_b = dict(sorted(pagerank_b.items()))
for node, score in sorted_pagerank_b.items():
    print(f"  {node}: {score:.8f}") # Drukujemy więcej miejsc po przecinku
print("-" * 40)

# --- Porównanie i wnioski ---

print("\n--- Porównanie wyników ---")
print("Oczekuje się, że wyniki z obu metod będą bardzo podobne.")
print("Metoda (a) jest symulacyjna i jej dokładność zależy od liczby kroków.")
print("Metoda (b) jest analityczna i dąży do dokładnego rozwiązania po osiągnięciu zbieżności.")
print("Drobne różnice między wynikami metody (a) i (b) są normalne ze względu na symulacyjny charakter metody (a).")

# Można obliczyć różnicę normy L1 między wynikami
# Upewniamy się, że wierzchołki są w tej samej kolejności
scores_a = np.array([sorted_pagerank_a[node] for node in all_nodes])
scores_b = np.array([sorted_pagerank_b[node] for node in all_nodes])

difference = np.linalg.norm(scores_a - scores_b, ord=1)
print(f"Norma L1 różnicy między wynikami (a) i (b): {difference:.10f}")
print("-" * 40)
