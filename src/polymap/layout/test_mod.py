from polymap.geometry.ortho import FancyOrthoDomain
from polymap.geometry.shapely_helpers import (
    get_coords_from_shapely_polygon,
    needs_simplifying,
)
from polymap.layout.interfaces import Layout, create_layout_from_json
import shapely as sp
from polymap.layout.graph import (
    create_graph_for_all_surfaces_along_axis,
    plot_graph,
)
import matplotlib.pyplot as plt

import networkx as nx

from polymap.visuals import plot_polygon


def print_nbs_data():
    pass
    # print(
    #     {(u, v): round(data["difference"], 2) for (u, v, data) in Gy.edges(data=True)}
    # )


def plot_graph2(layout, Gx: nx.DiGraph, Gy: nx.DiGraph):
    fig, (ax1, ax2) = plt.subplots(ncols=2, layout="tight", figsize=(12, 7))
    ax1.set_title("Gx")
    ax2.set_title("Gy")
    plot_graph(layout, Gx, ax1)
    plot_graph(layout, Gy, ax2)
    plt.show()


def plot_two_polygon(p1: sp.Polygon, p2: sp.Polygon, t1="", t2=""):
    fig, (ax1, ax2) = plt.subplots(ncols=2, layout="tight", figsize=(12, 7))
    ax1.set_title(t1)
    ax2.set_title(t2)
    plot_polygon(p1, ax1)
    plot_polygon(p2, ax2)
    plt.show()


def simplify_layout(layout: Layout):
    TOLERANCE = 0.5
    simplified_polys = [sp.simplify(i.polygon, TOLERANCE) for i in layout.domains]
    new_domains = [
        FancyOrthoDomain(get_coords_from_shapely_polygon(i), d.name)
        for d, i in zip(layout.domains, simplified_polys)
    ]
    return Layout(new_domains)


if __name__ == "__main__":
    # layout = create_layout_from_dict(sample_layout)
    layout = create_layout_from_json("48205")
    dom = layout.get_domain("room_7")
    print(needs_simplifying(dom))
    new_layout = simplify_layout(layout)
    # plot_two_polygon(dom.polygon, simple_dom)
    layout.plot_layout()
    new_layout.plot_layout()
    plt.show()
    # print(layout)

    Gx = create_graph_for_all_surfaces_along_axis(new_layout, "X")
    # fig, (ax1, ax2) = plt.subplots(ncols=2, layout="tight", figsize=(12, 7))
    # plot_graph(Gx.layout, Gx.G, ax1)
    # plt.show()

    # print(Gx.updated_layout)
    # Gy = create_graph_for_all_surfaces_along_axis(layout, "Y")
    # plot_graph(Gy.layout, Gy.G, ax2)
    # plt.show()
    # print(Gy.nbs_dict)
    # # Gy.updated_layout.plot_layout()
    # plot_graph2(Gy.layout, Gx.G, Gy.G)
