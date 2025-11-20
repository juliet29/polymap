import networkx as nx
from polymap.interfaces import GraphPairs
from polymap.geometry.surfaces import Surface
from polymap.geometry.surfaces import FancyRange
from polymap.layout.interfaces import Layout
from polymap.layout.neighbors import get_nbs_for_surf
from matplotlib.axes import Axes as MPLAxes
from polymap.geometry.vectors import Axes
from pipe import where, sort
from dataclasses import dataclass

DELTA = "delta"


def collect_node_nbs(G: nx.DiGraph) -> GraphPairs:
    nb_dict = {}
    for node in G.nodes:
        nbs = set(G.neighbors(node))
        if nbs:
            nb_dict[node] = list(nbs)
    return nb_dict


@dataclass
class AxGraph:
    G: nx.DiGraph
    ax: Axes
    layout: Layout

    def get_delta(self, nb1: str, nb2: str):
        for nb in [nb1, nb2]:
            assert nb in self.G.nodes

        return self.G.edges[(nb1, nb2)][DELTA]

    def get_neighors(self, node: str):
        return list(self.G.neighbors(node))

    @property
    def roots(self):
        return [n[0] for n in self.G.in_degree if n[1] == 0]

    @property
    def domains(self):
        return self.layout.domains

    @property
    def nb_pairs(self):
        return collect_node_nbs(self.G)


def create_graph_for_surface(
    layout: Layout,
    surf: Surface,
):
    nbs = get_nbs_for_surf(layout, surf)
    G = nx.DiGraph()
    for nb in nbs:
        delta = FancyRange(surf.location, nb.location).size
        G.add_edge(str(surf), str(nb), delta=delta)

    return G


def create_graph_for_all_surfaces_along_axis(layout: Layout, axis: Axes):
    surfaces = list(
        layout.get_surfaces(substantial_only=True)
        | where(lambda x: x.direction_axis == axis)
        | where(lambda x: x.direction.name == "north" or x.direction.name == "east")
        | sort(key=lambda x: x.location)
    )

    graphs = [
        create_graph_for_surface(layout, i)
        for i in surfaces  # TODO this should depend on the axis..
    ]
    G = nx.compose_all(graphs)
    return AxGraph(G, axis, layout)


# TODO -> potential for creating a dataclass...
# graph should return its axis maybe


def create_graph_for_layout(layout: Layout):
    Gx = create_graph_for_all_surfaces_along_axis(layout, "X")
    Gy = create_graph_for_all_surfaces_along_axis(layout, "Y")

    return Gx, Gy


def create_graph_positions(layout: Layout):
    return {str(i): i.centroid.as_tuple for i in layout.get_surfaces()}


def plot_graph(layout: Layout, G: nx.DiGraph, ax: MPLAxes):
    pos = create_graph_positions(layout)
    nx.draw_networkx(G, pos, ax=ax)
    edge_labels = {(u, v): round(data[DELTA], 2) for (u, v, data) in G.edges(data=True)}

    nx.draw_networkx_edge_labels(G, pos, edge_labels, ax=ax)
    return ax
