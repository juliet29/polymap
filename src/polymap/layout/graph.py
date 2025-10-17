import networkx as nx
from polymap.geometry.surfaces import Surface
from rich import print
from polymap.geometry.surfaces import FancyRange
from polymap.layout.interfaces import Layout
from polymap.layout.neighbors import get_nbs_for_surf
from matplotlib.axes import Axes as MPLAxes
from polymap.geometry.vectors import Axes
from pipe import where
from dataclasses import dataclass
from copy import deepcopy
from utils4plans.lists import chain_flatten


@dataclass
class AxGraph:
    G: nx.DiGraph
    ax: Axes
    layout: Layout

    @property
    def roots(self):
        return [n[0] for n in self.G.in_degree if n[1] == 0]

    def get_neighbors(self, node):
        return list(self.G.neighbors(node))

    def calc_delta(self, n1, n2):
        return self.G.edges[(n1, n2)]["delta"]

    def collect_domain_updates_for_node(self, node: str):
        def create_new_domain_for_nb(
            nb: str,
        ):
            delta = self.calc_delta(node, nb)
            surface = self.layout.get_surface_by_name(nb)
            domain = self.layout.get_domain(surface.domain_name)
            return domain.update_surface(surface, delta)

        return [create_new_domain_for_nb(i) for i in self.get_neighbors(node)]

    @property
    def updated_domains(self):
        return chain_flatten(
            [self.collect_domain_updates_for_node(i) for i in self.roots]
        )

    @property
    def updated_layout(self):
        return self.layout.update_layout(self.updated_domains)

    @property
    def nbs_dict(self):
        return collect_node_nbs(self.G)


def create_graph_for_surface(
    layout: Layout,
    surf: Surface,
):
    nbs = get_nbs_for_surf(layout, surf)
    G = nx.DiGraph()
    for nb in nbs:
        delta = FancyRange(nb.location, surf.location).size
        G.add_edge(str(surf), str(nb), delta=delta)

    return G


def create_graph_for_all_surfaces_along_axis(layout: Layout, axis: Axes):
    surfaces = list(
        layout.surfaces
        | where(lambda x: x.direction_axis == axis)
        | where(lambda x: x.direction.name == "south" or x.direction.name == "west")
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
    Gx.updated_layout.plot_layout()
    Gy = create_graph_for_all_surfaces_along_axis(layout, "Y")

    return Gx, Gy


def create_graph_positions(layout: Layout):
    return {str(i): i.centroid.as_tuple for i in layout.surfaces}


def plot_graph(layout: Layout, G: nx.DiGraph, ax: MPLAxes):
    pos = create_graph_positions(layout)
    nx.draw_networkx(G, pos, ax=ax)
    edge_labels = {
        (u, v): round(data["delta"], 2) for (u, v, data) in G.edges(data=True)
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
