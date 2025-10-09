import networkx as nx
from polymap.geometry.surfaces import Surface
from rich import print
from polymap.geometry.surfaces import FancyRange
from polymap.layout.interfaces import Layout
from polymap.layout.neighbors import get_nbs_for_surf
from matplotlib.axes import Axes as MPLAxes
from polymap.geometry.vectors import Axes


def create_graph_for_surface(
    layout: Layout,
    surf: Surface,
):
    nbs = get_nbs_for_surf(layout, surf)
    G = nx.DiGraph()
    for nb in nbs:
        difference = FancyRange(nb.location, surf.location).size
        G.add_edge(str(surf), str(nb),  difference=difference)

    return G


def create_graph_for_all_surfaces_along_axis(layout: Layout, axis: Axes) -> nx.DiGraph:
    graphs = [
        create_graph_for_surface(layout, i)
        for i in layout.surfaces
        if i.direction_axis == axis
    ]
    G = nx.compose_all(graphs)
    return G


def create_graph_positions(layout: Layout):
    return {str(i): i.centroid.as_tuple for i in layout.surfaces}


def plot_graph(layout: Layout, G: nx.DiGraph, ax: MPLAxes):
    pos = create_graph_positions(layout)
    nx.draw_networkx(G, pos, ax=ax)
    edge_labels = {
        (u, v): round(data["difference"], 2) for (u, v, data) in G.edges(data=True)
    }
    nx.draw_networkx_edge_labels(G, pos, edge_labels, ax=ax)
    return ax

def collect_node_nbs(G: nx.DiGraph):
    nb_dict = {}
    for node in G.nodes:
        nbs = set(G.neighbors(node))
        if nbs:
            nb_dict[node] = nbs
    return nb_dict