from dataclasses import dataclass

from rich.pretty import pretty_repr
from polymap.geometry.surfaces import Surface
from polymap.geometry.ortho import FancyOrthoDomain
from typing import Iterable, TypeVar
import networkx as nx
from utils4plans.lists import pairwise
from polymap.interfaces import make_repr_obj

T = TypeVar("T")


@dataclass
class DomainGraph:
    graph: nx.DiGraph


@dataclass
class NodeData:
    is_small: bool = False
    surface: Surface | None = None

    @property
    def repr_dict(self):
        def fx():
            yield "surface_name", self.surface.name if self.surface else ""
            yield "is_small", self.is_small

        return make_repr_obj(fx)

    # def __repr__(self):
    #     def fx():
    #         yield "is_small", self.is_small
    #         yield "surface_name", self.surface.name if self.surface else ""
    #
    #     return make_repr_obj(fx, self)


@dataclass(frozen=True)
class SurfaceNode:
    data: NodeData


#


def create_cycle_graph(nodes_: Iterable[T]):

    nodes = list(nodes_)
    node_cycle = nodes + [nodes[0]]

    # G: nx.DiGraph[SurfaceNode] = nx.DiGraph()
    G = nx.DiGraph()
    for i, j in pairwise(node_cycle):
        G.add_edge(i, j)

    return G


def find_directed_edges(G: nx.DiGraph, nodes: Iterable[T]):
    sg = G.subgraph(nodes)
    # TODO: some stronger conditions on this.. this is assuming that everuthing is connected..
    return list(sg.edges)


def order_nodes_based_on_edges(G: nx.DiGraph, nodes: Iterable[T]):
    def nodes_from_edges(edges_: Iterable[tuple[T, T]]):
        edges = list(edges_)
        n1 = [i[0] for i in edges] + [edges[-1][1]]
        return n1

    directed_edges = find_directed_edges(G, nodes)
    return nodes_from_edges(directed_edges)


def find_small_node_groups(G: nx.DiGraph):
    nodes = [n for n, d in G.nodes(data=True) if d["data"].is_small]
    sg = G.subgraph(nodes)
    components = nx.connected_components(sg.to_undirected())

    return list(components)


def find_small_node_surfaces(G: nx.DiGraph, nodes: Iterable[str]) -> list[Surface]:
    def find(node: str):
        res = G.nodes[node].get("data")
        assert isinstance(res, NodeData)
        s = res.surface
        assert s
        return s

    return [find(n) for n in nodes]


def handle_components(G: nx.DiGraph, nodes_: Iterable[str]):
    nodes = list(nodes_)
    if len(nodes) >= 2:
        ordered_nodes = order_nodes_based_on_edges(G, nodes)
    else:
        ordered_nodes = nodes
    return find_small_node_surfaces(G, ordered_nodes)


def create_surface_graph_for_domain(domain: FancyOrthoDomain):

    surf_names = [i.name for i in domain.surfaces]
    G = create_cycle_graph(surf_names)
    node_data = {
        name: {"data": NodeData(is_small=surf.is_small, surface=surf)}
        for name, surf in zip(surf_names, domain.surfaces)
    }
    nx.set_node_attributes(G, node_data)
    return G


def get_surface(G: nx.Graph, node: str):
    data = G.nodes[node].get("data")
    assert isinstance(data, NodeData)
    s = data.surface
    assert s
    return s


def get_predecesor(G: nx.DiGraph, node: object):
    res = list(G.predecessors(node))[0]
    return get_surface(G, res)


def get_successor(G: nx.DiGraph, node: object):
    res = list(G.successors(node))[0]
    return get_surface(G, res)


def repr_graph(G: nx.DiGraph):
    fd = {}
    for node, d in G.nodes(data=True):
        # TODO: can clean up with get method..
        data = d["data"]
        assert isinstance(data, NodeData)
        fd[node] = data.repr_dict
    return pretty_repr(fd, expand_all=True)

    # def fx():
    #     for node, d in G.nodes(data=True):
    #         data = d["data"]
    #         assert isinstance(data, NodeData)
    #         return data.__repr__
    #
    # return make_repr_obj(fx, "SurfaceGraph")
