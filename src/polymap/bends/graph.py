from copy import deepcopy
from dataclasses import dataclass
from utils4plans.lists import get_unique_one
from utils4plans.sets import set_difference


from loguru import logger
from rich.pretty import pretty_repr
from polymap.geometry.surfaces import Surface
from polymap.geometry.ortho import FancyOrthoDomain
from typing import Iterable, TypeVar
import networkx as nx
from utils4plans.lists import pairwise
from polymap.bends.utils import make_repr_obj

T = TypeVar("T")


@dataclass
class DomainGraph:
    graph: nx.DiGraph


@dataclass
class NodeData:
    is_small: bool = False
    surface: Surface | None = None
    is_nb_small: bool = False
    is_nb2_small: bool = False

    @property
    def repr_dict(self):
        def fx():
            yield "surface_name", self.surface.name_w_domain if self.surface else ""
            yield "is_small", self.is_small
            yield "is_nb_small", self.is_nb_small
            yield "is_nb2_small", self.is_nb2_small

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


def get_nodes_data(G: nx.DiGraph, node: str):
    data = G.nodes[node].get("data")
    assert isinstance(data, NodeData)
    d: NodeData = data
    return d


def get_predecesor(G: nx.DiGraph, node: object):
    res = list(G.predecessors(node))[0]
    return get_surface(G, res)


def get_successor(G: nx.DiGraph, node: object):
    res = list(G.successors(node))[0]
    return get_surface(G, res)


def get_successor_node(G: nx.DiGraph, node: object):
    res = list(G.successors(node))
    assert len(res) == 1, f"Expected one successor, but got {res}"
    # should assert num of succesors = 1
    return res[0]


def create_cycle_graph(nodes_: Iterable[T]):
    nodes = list(nodes_)
    node_cycle = nodes + [nodes[0]]

    # G: nx.DiGraph[SurfaceNode] = nx.DiGraph()
    G = nx.DiGraph()
    for i, j in pairwise(node_cycle):
        G.add_edge(i, j)

    return G


def create_surface_graph_for_domain(domain: FancyOrthoDomain):

    surf_names = [i.name_w_domain for i in domain.surfaces]
    G = create_cycle_graph(surf_names)
    node_data = {
        name: {"data": NodeData(is_small=surf.is_small, surface=surf)}
        for name, surf in zip(surf_names, domain.surfaces)
    }
    nx.set_node_attributes(G, node_data)
    return G


def update_small_nbs(G_: nx.DiGraph):
    def check_nb_is_small(G: nx.DiGraph, nb: str):
        data = get_nodes_data(G, nb)
        return data.is_small

    def update(G: nx.DiGraph, node: str):
        data = get_nodes_data(G, node)
        n1 = get_successor_node(G, node)
        data.is_nb_small = check_nb_is_small(G, n1)

        n2 = get_successor_node(G, n1)
        data.is_nb2_small = check_nb_is_small(G, n2)

    G = deepcopy(G_)
    for node in G.nodes:
        update(G, node)

    return G


def find_small_node_groups(G: nx.DiGraph):
    nodes = [n for n, d in G.nodes(data=True) if d["data"].is_small]
    sg = G.subgraph(nodes)
    components = nx.connected_components(sg.to_undirected())

    return list(components)


def find_ends_of_a_directed_graph(G: nx.DiGraph):
    root = get_unique_one(G.nodes, lambda x: len(list(G.predecessors(x))) == 0)
    end = get_unique_one(G.nodes, lambda x: len(list(G.successors(x))) == 0)
    return root, end


def order_nodes_based_on_graph(G: nx.DiGraph, nodes_: Iterable[T]):
    nodes = list(nodes_)
    nodes_to_remove = set_difference(G.nodes, nodes)
    sg = deepcopy(G)
    sg.remove_nodes_from(nodes_to_remove)

    logger.trace(sg.nodes)
    if len(nodes) > 2:
        root, end = find_ends_of_a_directed_graph(sg)
        paths = list(nx.shortest_simple_paths(sg, root, end))
        logger.trace(paths)
        assert len(paths) == 1
        return paths[0]

    logger.trace(G.edge_subgraph(sg.edges).edges)
    assert sg.order() == 2
    assert len(sg.edges) == 1
    e = list(sg.edges)[0]
    return [e[0], e[1]]
    # TODO: some stronger conditions on this.. this is assuming that everuthing is connected..
    return list(sg.edges)


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
        ordered_nodes = order_nodes_based_on_graph(G, nodes)
        logger.trace(pretty_repr({"orig_nodes": nodes, "ordered": ordered_nodes}))
    else:
        ordered_nodes = nodes
    return find_small_node_surfaces(G, ordered_nodes)


def get_surface(G: nx.Graph, node: str):
    data = G.nodes[node].get("data")
    assert isinstance(data, NodeData)
    s = data.surface
    assert s
    return s


def repr_graph(G: nx.DiGraph):
    fd = {}
    for node, d in G.nodes(data=True):
        # TODO: can clean up with get method..
        data = d["data"]
        assert isinstance(data, NodeData)
        fd[node] = data.repr_dict
    return pretty_repr(fd, expand_all=True)
