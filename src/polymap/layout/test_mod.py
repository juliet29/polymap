from polymap.layout.interfaces import create_layout_from_dict, create_layout_from_json
from polymap.layout.neighbors import get_candidate_surface_neighbors, get_nbs_for_surf
from polymap.examples.layout import layout as sample_layout
from rich import print
from polymap.layout.graph import (
    create_graph_for_surface,
    create_graph_for_all_surfaces_along_axis,
    plot_graph,
    collect_node_nbs,
)
import matplotlib.pyplot as plt
from polymap.visuals import plot_polygon

import networkx as nx


def plot_graph2(layout, Gx: nx.DiGraph, Gy: nx.DiGraph):
    fig, (ax1, ax2) = plt.subplots(ncols=2, layout="tight", figsize=(12, 7))
    ax1.set_title("Gx")
    ax2.set_title("Gy")
    plot_graph(layout, Gx, ax1)
    plot_graph(layout, Gy, ax2)
    plt.show()


if __name__ == "__main__":
    # layout = create_layout_from_dict(sample_layout)
    layout = create_layout_from_json("48205")
    # layout.plot_layout()
    # print(layout)

    Gx = create_graph_for_all_surfaces_along_axis(layout, "X")
    print(Gx.updated_layout)
    Gy = create_graph_for_all_surfaces_along_axis(Gx.updated_layout, "Y")
    print(Gy.nbs_dict)
    # Gy.updated_layout.plot_layout()
    # plot_graph2(Gy.updated_layout, Gx.G, Gy.G)

    # Gy = create_graph_for_all_surfaces_along_axis(layout, "Y")
    # # c = collect_node_nbs(Gy)
    # # print(c)
    # # # print(list(Gy.neighbors("blue-north_0")))
    # plot_graph2(layout, Gx, Gy)
    # print(
    #     {(u, v): round(data["difference"], 2) for (u, v, data) in Gy.edges(data=True)}
    # )

    # surf = layout.get_domain("red").get_surface("south", 1)
    # nbs = get_nbs_for_surf(layout, surf)
    # g = create_graph_for_surface(layout, surf)
