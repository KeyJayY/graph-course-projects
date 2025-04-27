import networkx as nx
import matplotlib.pyplot as plt
import matplotlib
import os
import math

matplotlib.use("TkAgg")


def draw_circle_graph(G, radius, name, weights=False):
    if not os.path.isdir("imgs"):
        os.mkdir("imgs")

    pos = {}
    n = len(G.nodes())
    for i, node in enumerate(G.nodes()):
        angle = 2 * math.pi / n
        pos[node] = (radius * math.cos(angle * i), radius * math.sin(angle * i))

    nx.draw(
        G,
        pos,
        with_labels=True,
        node_color="skyblue",
        node_size=1500,
        font_size=12,
        font_weight="bold",
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

    plt.savefig(os.path.join("imgs", name))
    plt.clf()
