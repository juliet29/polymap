from copy import deepcopy
from polymap.visuals.visuals import plot_domain_with_surfaces
from rich.pretty import pretty_repr
from utils4plans.sets import set_equality
import networkx as nx

from polymap.bends.bends import assign_bends, check_is_pi_two, identify_pi_twos
from polymap.bends.graph import (
    NodeData,
    create_cycle_graph,
    create_surface_graph_for_domain,
    order_nodes_based_on_graph,
    find_small_node_groups,
    handle_components,
    repr_graph,
    update_small_nbs,
)
from loguru import logger

from polymap.examples.bends import PiExamples
from polymap.geometry.ortho import FancyOrthoDomain
from utils4plans.logconfig import logset


def test_create_cycle_graph():
    expected_edges = [(0, 1), (1, 2), (2, 0)]
    G = create_cycle_graph(range(3))
    logger.debug(G.edges)
    logger.debug(expected_edges)
    logger.debug(type(G.edges))

    assert list(G.edges) == expected_edges


def test_find_ordered_nodes():
    G = create_cycle_graph(range(5))
    logger.debug(G.edges)

    comp = {0, 4, 1}
    nodes = order_nodes_based_on_graph(G, comp)
    expected_nodes = [4, 0, 1]
    logger.debug(nodes)
    assert nodes == expected_nodes


class TestSimpleGraph:
    num = 5
    G = create_cycle_graph(range(num))
    node_data = {i: {"data": NodeData(is_small=False)} for i in range(num)}
    nx.set_node_attributes(G, node_data)

    test_nodes = {0, 4, 2}

    for node in test_nodes:
        G.nodes(data=True)[node]["data"].is_small = True

    def test_find_small_groups(self):
        node_groups = find_small_node_groups(self.G)
        logger.debug(node_groups)
        expected_groups = [{0, 4}, {2}]
        assert expected_groups == node_groups

    def test_find_edges(self):
        node_groups = find_small_node_groups(self.G)
        valid_node_groups = [i for i in node_groups if len(i) >= 2]
        nodes = order_nodes_based_on_graph(self.G, valid_node_groups[0])
        logger.debug(nodes)

        expected_nodes = [4, 0]
        assert expected_nodes == nodes


class TestDomainSurfaceGraph:
    pe = PiExamples()
    domain = FancyOrthoDomain.from_tuple_list(pe.one)
    G = create_surface_graph_for_domain(domain)

    def show_domain(self):
        plot_domain_with_surfaces(self.domain)

    def print_graph(self):
        logger.debug(repr_graph(self.G))

    def test_can_make_graph(self):
        assert len(self.G.nodes) > 2
        assert len(self.G.edges) > 2

    def test_can_get_components_one(self):
        components = find_small_node_groups(self.G)
        logger.debug(components)
        surfs = handle_components(self.G, components[0])

        logger.debug(pretty_repr(surfs))

        expected_surf = self.domain.get_surface("north", 1)

        logger.debug(pretty_repr(expected_surf))
        assert surfs[0] == expected_surf

    def test_can_get_components_many(self):
        G = deepcopy(self.G)
        node_data = G.nodes["-west_1"].get("data")
        assert node_data
        node_data.is_small = True

        components = find_small_node_groups(G)
        logger.debug(components)
        surfs = handle_components(G, components[0])

        logger.debug(pretty_repr(surfs, expand_all=True))

        expected_surfs = [
            self.domain.get_surface("north", 1),
            self.domain.get_surface("west", 1),
        ]

        assert set_equality(expected_surfs, surfs)

    def test_make_bends(self):
        bh = assign_bends(self.domain)
        logger.debug(bh.summary)


class TestPi2Identify:
    pe = PiExamples()
    domain = FancyOrthoDomain.from_tuple_list(pe.two)
    G = create_surface_graph_for_domain(domain)
    G_updated = update_small_nbs(G)

    def show_domain(self):
        plot_domain_with_surfaces(self.domain)

    def print_graph(self):
        # plot_domain_with_surfaces(self.domain, "pi two example")
        logger.debug(repr_graph(self.G_updated))

    def test_check_of_pi_two(self):
        # TODO: changes names of surfaces.. => Have to fix tests after..
        expected_node = "-east_1"
        res = check_is_pi_two(self.G_updated, expected_node)
        assert res

    def test_make_pi_two_group(self):
        bends = identify_pi_twos(self.domain, self.G_updated)
        assert len(bends) == 1
        # for b in bends:
        #     logger.info(b.surface_names)


if __name__ == "__main__":
    logset()
    t = TestPi2Identify()
    t.show_domain()
    t.print_graph()
    t.test_check_of_pi_two()
    # t.print_graph()
    # t.test_check_of_pi_two()
