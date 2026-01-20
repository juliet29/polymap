from loguru import logger
import networkx as nx
from rich.pretty import pretty_repr
from utils4plans.lists import chain_flatten
from utils4plans.sets import set_difference
from polymap.geometry.surfaces import Surface
from polymap.geometry.surfaces import FancyRange
from polymap.geometry.layout import Layout
from polymap.layout.neighbors import get_nbs_for_surf
from polymap.geometry.vectors import Axes
from pipe import where, sort
from polymap.layout.interfaces import Edge, EdgeData, EdgeDataDiGraph, AxGraph


def compute_delta_between_surfs(s1: Surface, s2: Surface):
    delta = FancyRange(s1.location, s2.location).size
    return delta


def create_graph_for_surface(
    layout: Layout,
    surf: Surface,
):
    nbs = get_nbs_for_surf(layout, surf)
    G = EdgeDataDiGraph()  # nx.DiGraph()
    for nb in nbs:
        delta = compute_delta_between_surfs(surf, nb)
        # delta = FancyRange(surf.location, nb.location).size
        G.add_edge(str(surf), str(nb), data=EdgeData(delta, surf.domain_name))

    # TODO: modify delta based on the overarching graph...., basically, have opportunities for bi-directional moves..
    return G


def create_move_graph(layout: Layout, G: EdgeDataDiGraph):
    def transform(e: Edge):
        new_delta = -1 * (e.data.delta - min_edge.data.delta)
        new_domain = layout.get_surface_by_name(e.v).domain_name

        new_data = EdgeData(delta=new_delta, domain_name=new_domain)
        new_edge = Edge(e.v, e.u, new_data)
        return new_edge

    if len(G.edges) <= 1:
        return G

    # all the deltas are the same -> just need to move one..
    deltas = [i.data.delta for i in G.edge_data()]
    if len(set(deltas)) == 1:
        new_G = EdgeDataDiGraph()
        e = G.edge_data()[0]
        new_G.add_edge(e.u, e.v, data=e.data)
        return new_G

    min_edge = sorted(G.edge_data(), key=lambda x: x.data.delta)[0]
    other_edges = set_difference(G.edge_data(), [min_edge])
    new_edges = [transform(e) for e in other_edges] + [min_edge]

    new_G = EdgeDataDiGraph()
    for e in new_edges:
        if abs(e.data.delta) > 0:
            new_G.add_edge(e.u, e.v, data=e.data)
    # logger.info(pretty_repr(new_G.edge_data()))

    return new_G


def create_individual_graphs(layout: Layout, axis: Axes):
    surfaces = list(
        layout.get_surfaces(substantial_only=True)
        | where(lambda x: x.perpendicular_axis == axis)
        | where(lambda x: x.direction.name == "north" or x.direction.name == "east")
        | sort(key=lambda x: x.location)
    )

    graphs = [create_graph_for_surface(layout, i) for i in surfaces]
    return graphs


def create_graph_for_all_surfaces_along_axis(layout: Layout, axis: Axes):
    graphs = create_individual_graphs(layout, axis)

    G = nx.compose_all(graphs)
    return AxGraph(G, axis, layout)


def summarize_graph_list(graphs: list[EdgeDataDiGraph]):
    res = chain_flatten([g.edge_summary_list() for g in graphs])
    logger.info(pretty_repr(res))


def create_move_graph_for_all_surfaces_along_axis(layout: Layout, axis: Axes):
    graphs = create_individual_graphs(layout, axis)
    summarize_graph_list(graphs)
    # move_graphs = [create_move_graph(layout, g) for g in graphs]
    # summarize_graph_list(move_graphs)

    G = nx.compose_all(graphs)
    return AxGraph(G, axis, layout)


# TODO -> potential for creating a dataclass...
# graph should return its axis maybe
