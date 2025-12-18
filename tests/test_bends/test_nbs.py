import networkx as nx

from polymap.bends.graph import (
    NodeData,
    create_cycle_graph,
    create_surface_graph_for_domain,
    find_directed_edges,
    find_small_node_groups,
    handle_components,
    repr_graph,
)
from loguru import logger

from polymap.bends.examples import PiExamples
from polymap.geometry.ortho import FancyOrthoDomain
from polymap.logconf import logset


def test_create_cycle_graph():
    expected_edges = [(0, 1), (1, 2), (2, 0)]
    G = create_cycle_graph(range(3))
    logger.debug(G.edges)
    logger.debug(expected_edges)
    logger.debug(type(G.edges))

    assert list(G.edges) == expected_edges


def test_find_directed_edges():
    G = create_cycle_graph(range(5))
    logger.debug(G.edges)

    comp = {0, 4, 1}
    edges = find_directed_edges(G, comp)
    expected_edges = [(0, 1), (4, 0)]
    logger.debug(edges)
    assert edges == expected_edges


class TestSimpleGraph:
    def __init__(self) -> None:
        num = 5
        G = create_cycle_graph(range(num))
        node_data = {i: {"data": NodeData(is_small=False)} for i in range(num)}
        nx.set_node_attributes(G, node_data)

        test_nodes = {0, 4, 2}

        for node in test_nodes:
            G.nodes(data=True)[node]["data"].is_small = True
        self.G = G

    def test_find_small_groups(self):
        node_groups = find_small_node_groups(self.G)
        logger.debug(node_groups)
        expected_groups = [{0, 4}, {2}]
        assert expected_groups == node_groups

    def test_find_edges(self):
        node_groups = find_small_node_groups(self.G)
        valid_node_groups = [i for i in node_groups if len(i) >= 2]
        edges = find_directed_edges(self.G, valid_node_groups[0])
        logger.debug(edges)

        expected_edges = [(4, 0)]
        assert expected_edges == edges


class TestDomain:
    def __init__(self):
        pe = PiExamples()
        domain = FancyOrthoDomain.from_tuple_list(pe.one)
        self.domain = domain
        self.G = create_surface_graph_for_domain(domain)

    def print_graph(self):
        logger.debug(repr_graph(self.G))

    def test_can_make_graph(self):
        assert len(self.G.nodes) > 2
        assert len(self.G.edges) > 2

    def test_can_get_components_one(self):
        components = find_small_node_groups(self.G)
        surfs = handle_components(self.G, components[0])

        logger.debug(surfs)

        expected_surf = self.domain.get_surface("north")
        assert surfs[0] == expected_surf


# def test_create_surface_graph():
#     pe = PiExamples()
#     domain = FancyOrthoDomain.from_tuple_list(pe.one)
#     G = create_surface_graph_for_domain(domain)
#     logger.debug(G)
#     logger.debug(G.edges)
#     # logger.debug(
#     #     pretty_repr(G.nodes(data=True), max_width=10, indent_size=20, expand_all=True)
#     # )
#     # logger.debug(G.nodes(data=True))
#     logger.debug(repr_graph(G))


if __name__ == "__main__":
    logset()
    logger.debug("hekko?")
    print("hi")
    t = TestDomain()
    t.test_can_get_components_one()
