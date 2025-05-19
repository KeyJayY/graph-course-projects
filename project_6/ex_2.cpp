#include <iostream>
#include <vector>
#include <cmath>
#include <random>
#include <algorithm>
#include <numeric>
#include <chrono>
#include <limits>
#include <iomanip> // Do formatowania wyjścia

// Struktura do reprezentacji punktu
struct Point
{
    int x, y;
};

// Funkcja obliczająca odległość Euklidesową między dwoma punktami
double euclidean_distance(const Point &p1, const Point &p2)
{
    double dx = p1.x - p2.x;
    double dy = p1.y - p2.y;
    return std::sqrt(dx * dx + dy * dy);
}

// Funkcja obliczająca całkowitą długość ścieżki
double calculate_tour_length(const std::vector<int> &tour, const std::vector<Point> &points)
{
    double length = 0.0;
    int num_points = tour.size();

    if (num_points < 2)
    {
        return 0.0; // Pusta ścieżka lub ścieżka z jednym punktem ma zerową długość
    }
    if (num_points == 2)
    {
        // Dla 2 punktów, ścieżka to 0 -> 1 -> 0
        return 2.0 * euclidean_distance(points[tour[0]], points[tour[1]]);
    }

    // Obliczanie odległości między kolejnymi punktami w ścieżce
    for (int i = 0; i < num_points; ++i)
    {
        int p1_index = tour[i];
        int p2_index = tour[(i + 1) % num_points]; // Używamy modulo dla zamkniętej ścieżki (ostatni do pierwszego)
        length += euclidean_distance(points[p1_index], points[p2_index]);
    }
    return length;
}

// Funkcja wykonująca operację 2-opt
std::vector<int> two_opt_swap(const std::vector<int> &tour, int i, int j)
{
    // Tworzymy kopię ścieżki, żeby nie modyfikować oryginału
    std::vector<int> new_tour = tour;

    // Odwracamy segment od i do j włącznie
    // std::reverse działa na iteratorach: [first, last)
    std::reverse(new_tour.begin() + i, new_tour.begin() + j + 1);

    return new_tour;
}

// Algorytm symulowanego wyżarzania dla problemu komiwojażera
std::pair<std::vector<int>, double> simulated_annealing_tsp(
    const std::vector<Point> &points,
    double initial_temperature,
    double cooling_rate,
    int iterations_per_temp,
    int num_cooling_steps, // Zmieniono na liczbę etapów chłodzenia
    std::mt19937 &rng      // Generator liczb losowych
)
{
    int num_points = points.size();
    if (num_points < 2)
    {
        std::vector<int> tour(num_points);
        std::iota(tour.begin(), tour.end(), 0); // Wypełnij 0, 1, ..., num_points-1
        return {tour, 0.0};
    }

    // Inicjalizacja: losowa ścieżka początkowa (permutacja indeksów wierzchołków)
    std::vector<int> current_tour(num_points);
    std::iota(current_tour.begin(), current_tour.end(), 0);      // Wypełnij 0, 1, ..., num_points-1
    std::shuffle(current_tour.begin(), current_tour.end(), rng); // Losowa permutacja

    double current_length = calculate_tour_length(current_tour, points);

    // Najlepsza znaleziona ścieżka
    std::vector<int> best_tour = current_tour;
    double best_length = current_length;

    // Parametry wyżarzania
    double temperature = initial_temperature;

    std::cout << "--- Rozpoczecie symulowanego wyzarzania ---" << std::endl;
    std::cout << "Liczba wierzcholkow: " << num_points << std::endl;
    std::cout << std::fixed << std::setprecision(4);
    std::cout << "Wspolczynnik chlodzenia: " << cooling_rate << std::endl;
    std::cout << "Iteracji na temperature: " << iterations_per_temp << std::endl;
    std::cout << "Liczba etapow chlodzenia: " << num_cooling_steps << std::endl;
    std::cout << "Poczatkowa dlugosc sciezki: " << current_length << std::endl;

    int iteration_count = 0;
    // Generatory liczb losowych dla indeksów i prawdopodobieństwa
    std::uniform_int_distribution<> dist_indices(0, num_points - 1);
    std::uniform_real_distribution<> dist_prob(0.0, 1.0);

    // Główna pętla symulowanego wyżarzania (chłodzenie) - Na podstawie liczby etapów
    for (int step = 0; step < num_cooling_steps; ++step)
    {
        // Wykonaj wiele kroków (ruchów) przy obecnej temperaturze
        for (int iter = 0; iter < iterations_per_temp; ++iter)
        {
            iteration_count++;

            // Wygeneruj sąsiednie rozwiązanie przy użyciu operacji 2-opt
            // Losujemy dwa różne indeksy i, j z zakresu [0, num_points - 1]
            int i = dist_indices(rng);
            int j = dist_indices(rng);
            while (i == j)
            {
                j = dist_indices(rng);
            }

            // Upewniamy się, że i < j
            if (i > j)
            {
                std::swap(i, j);
            }

            // Używamy operacji 2-opt odwracającej segment tour[i...j]
            std::vector<int> new_tour = two_opt_swap(current_tour, i, j);
            double new_length = calculate_tour_length(new_tour, points);

            // Obliczenie różnicy energii (długości ścieżki)
            double delta_energy = new_length - current_length;

            // Zastosowanie kryterium Metropolisa-Hastingsa
            // Akceptuj nowe rozwiązanie, jeśli jest lepsze LUB
            // Akceptuj gorsze rozwiązanie z prawdopodobieństwem exp(-delta_energy / temperature)
            if (delta_energy < 0.0 || dist_prob(rng) < std::exp(-delta_energy / temperature))
            {
                current_tour = new_tour; // Akceptuj, kopiując wektor
                current_length = new_length;

                // Aktualizacja najlepszego znalezionego rozwiązania
                if (current_length < best_length)
                {
                    best_tour = current_tour; // Aktualizuj najlepszy, kopiując wektor
                    best_length = current_length;
                    // Opcjonalnie: drukuj postęp po znalezieniu lepszej ścieżki
                    // std::cout << "Iteracja " << iteration_count << ": Znaleziono lepszą ścieżkę o długości " << best_length << " przy T=" << temperature << std::endl;
                }
            }
        }

        // Chłodzenie: zmniejszenie temperatury
        temperature *= cooling_rate;
        // Opcjonalnie: drukuj postęp chłodzenia co N kroków
        // if ((step + 1) % 100 == 0) {
        //    std::cout << "Etap chłodzenia " << step + 1 << "/" << num_cooling_steps << ", T=" << temperature << ", Best Length=" << best_length << std::endl;
        // }
    }

std::cout << "--- Koniec symulowanego wyzarzania ---" << std::endl;
std::cout << "Calkowita liczba krokow (ruchow 2-opt): " << iteration_count << std::endl;

    return {best_tour, best_length};
}

int main()
{
    // --- Przykładowe dane z pliku (wczytane ręcznie/skopiowane) ---
    const std::string data_string = R"(
34 15
5 19
38 34
25 28
41 34
63 6
57 12
74 24
78 39
38 16
0 13
81 17
35 31
28 20
74 6
84 34
5 43
84 24
51 47
18 11
74 20
28 43
71 45
48 27
15 25
28 40
41 36
84 20
10 10
80 41
84 6
18 17
78 10
25 9
15 31
25 29
25 24
34 31
12 5
71 16
33 31
25 22
18 42
18 29
0 39
34 5
0 26
74 29
71 13
78 35
34 26
28 16
33 15
33 29
18 23
74 39
28 47
28 30
18 33
48 6
12 10
61 45
18 39
25 15
5 31
15 37
34 41
84 38
74 12
18 19
61 47
11 10
18 27
84 29
38 20
79 37
25 26
18 41
15 19
5 8
80 5
18 44
79 10
25 23
107 27
71 47
71 11
56 25
18 13
79 33
25 11
41 23
5 37
15 13
57 44
48 22
74 16
74 35
41 32
0 27
18 21
18 25
18 35
15 43
18 31
51 45
41 35
2 0
78 32
5 25
80 10
15 8
5 13
34 29
35 17
8 0
32 26
9 10
57 25
77 21
18 15
32 31
34 38
28 34
33 26
18 45
64 22
38 30
40 22
18 37
28 28
)";

    // Parsowanie danych do listy punktów (struktur Point)
    std::vector<Point> points_from_data;
    std::stringstream ss(data_string);
    int x, y;
    while (ss >> x >> y)
    {
        points_from_data.push_back({x, y});
    }

    std::cout << "Wczytano " << points_from_data.size() << " punktow z danych." << std::endl;

    // Inicjalizacja generatora liczb losowych
    unsigned seed = std::chrono::system_clock::now().time_since_epoch().count();
    std::mt19937 rng(seed);

    // Parametry algorytmu symulowanego wyżarzania
    // Możesz dostosować te parametry
    double sa_initial_temp = 10000.0;
    double sa_cooling_rate = 0.995;         // Wolniejsze chłodzenie dla lepszych wyników
    int sa_iterations_per_temp_factor = 50; // Mnożnik liczby iteracji na temperaturę
    int sa_num_cooling_steps = 5000;        // Liczba etapów chłodzenia (kontroluje czas wykonania)

    // Obliczenie liczby iteracji na temperaturę
    // Ustawiamy proporcjonalnie do liczby punktów (liniowo)
    int sa_iterations_per_temp = sa_iterations_per_temp_factor * points_from_data.size();

    // Ogranicz liczbę iteracji per temp, jeśli jest bardzo duża, dla przyspieszenia testów
    // sa_iterations_per_temp = std::min(sa_iterations_per_temp, 500000);

    std::cout << "Liczba iteracji na temperature: " << sa_iterations_per_temp << std::endl;
    long long total_estimated_moves = static_cast<long long>(sa_iterations_per_temp) * sa_num_cooling_steps;
    std::cout << "Calkowita szacowana liczba ruchow: " << total_estimated_moves << std::endl;

    // Uruchomienie algorytmu
    auto start_time = std::chrono::high_resolution_clock::now();
    std::pair<std::vector<int>, double> result = simulated_annealing_tsp(
        points_from_data,
        sa_initial_temp,
        sa_cooling_rate,
        sa_iterations_per_temp,
        sa_num_cooling_steps,
        rng // Przekazanie generatora
    );
    auto end_time = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> elapsed = end_time - start_time;

    std::vector<int> best_tour_indices = result.first;
    double min_tour_length = result.second;

    std::cout << "\n--- Wyniki Optymalizacji ---" << std::endl;
    std::cout << std::fixed << std::setprecision(4);
    std::cout << "Liczba wierzcholkow: " << points_from_data.size() << std::endl;
    std::cout << "Najkrotsza znaleziona dlugosc sciezki: " << min_tour_length << std::endl;

    // Drukujemy ścieżkę jako sekwencję indeksów wierzchołków
    std::cout << "Najlepsza znaleziona sciezka (indeksy wierzcholkow): [";
    for (size_t i = 0; i < best_tour_indices.size(); ++i)
    {
        std::cout << best_tour_indices[i] << (i == best_tour_indices.size() - 1 ? "" : ", ");
    }
    std::cout << "]" << std::endl;

    // Drukujemy ścieżkę jako sekwencję punktów (koordinaty)
    std::cout << "Najlepsza znaleziona sciezka (koordynaty):" << std::endl;
    std::cout << "[";
    size_t print_limit = 10; // Drukuj tylko kilka pierwszych i ostatnich punktów
    bool middle_dots = best_tour_indices.size() > 2 * print_limit;

    for (size_t i = 0; i < best_tour_indices.size(); ++i)
    {
        if (i < print_limit || (!middle_dots || i >= best_tour_indices.size() - print_limit))
        {
            int point_idx = best_tour_indices[i];
            std::cout << "(" << points_from_data[point_idx].x << ", " << points_from_data[point_idx].y << ")";
            if (i < best_tour_indices.size() - 1)
            {
                std::cout << ", ";
            }
        }
        else if (i == print_limit)
        {
            std::cout << "..., ";
        }
    }
    // Dodajemy powrót do punktu startowego na końcu dla wizualizacji cyklu
    if (!best_tour_indices.empty())
    {
        int start_point_idx = best_tour_indices[0];
        std::cout << " -> (" << points_from_data[start_point_idx].x << ", " << points_from_data[start_point_idx].y << ")";
    }

    std::cout << "]" << std::endl;

    std::cout << "\nCzas wykonania algorytmu: " << elapsed.count() << " sekundy." << std::endl;

    // Opcjonalnie: W C++ wizualizacja wymaga zewnętrznych bibliotek graficznych
    // lub zapisania wyników do pliku, który może być wizualizowany przez inne narzędzia (np. skrypt Python z matplotlib).

    return 0;
}
