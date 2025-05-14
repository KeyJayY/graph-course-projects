import networkx as nx
import matplotlib.pyplot as plt
import matplotlib
import os
import math

matplotlib.use("TkAgg")


def draw_circle_graph(G, radius, name, directory=None, weights=False, colors="skyblue"):
    if not os.path.isdir("imgs"):
        os.mkdir("imgs")

    if directory != None:
        if not os.path.isdir(os.path.join("imgs", directory)):
            os.mkdir(os.path.join("imgs", directory))

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
        arrows=is_directed,  # Dodaj strzałki tylko jeśli graf jest skierowany
        connectionstyle="arc3,rad=0.1",  # Łukowate krawędzie dla lepszej czytelności w grafach skierowanych
    )

    if weights:
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

    if directory != None:
        plt.savefig(os.path.join(os.path.join("imgs", directory), name))
    else:
        plt.savefig(os.path.join("imgs", name))
    plt.clf()
