from loguru import logger
from utils4plans.lists import chain_flatten
from polymap.geometry.modify.validate import InvalidPolygonError, validate_polygon
from polymap.bends.graph import (
    create_surface_graph_for_domain,
    find_small_node_groups,
    get_nodes_data,
    get_successor_node,
    handle_components,
    update_small_nbs,
)
from polymap.geometry.ortho import FancyOrthoDomain
from polymap.bends.interfaces import (
    BendHolder,
    KappaOne,
    KappaTwo,
    PiOne,
    PiThree,
    PiTwo,
)
import networkx as nx

from polymap.geometry.surfaces import Surface


def check_is_pi_two(G: nx.DiGraph, node: str):
    data = get_nodes_data(G, node)
    if data.is_small and data.is_nb2_small and not data.is_nb_small:
        return True


def identify_pi_twos(domain: FancyOrthoDomain, G_: nx.DiGraph):

    def make(node: str):
        n1 = get_successor_node(G, node)
        n2 = get_successor_node(G, n1)

        s1 = get_nodes_data(G, node).surface
        s2 = get_nodes_data(G, n2).surface
        assert s1 and s2
        return PiTwo.from_surfaces(domain, G, s1, s2)

    G = update_small_nbs(G_)

    bends = [make(node) for node in G.nodes if check_is_pi_two(G, node)]

    # only want those where are passing bend checks
    passing_bends = [i for i in bends if i.are_vectors_correct]
    return passing_bends


def is_part_of_pi_twos(bends: list[PiTwo], surface: Surface):
    pi2surfs = chain_flatten([[i.s1, i.s2] for i in bends])
    if surface in pi2surfs:
        return True


def assign_bends(domain: FancyOrthoDomain, domain_name: int | str = ""):

    bh = BendHolder()
    try:
        validate_polygon(domain.polygon, domain.name)
    except InvalidPolygonError as e:
        logger.error(
            f"Could not validate polygon, and could not assign bends for domain<{domain_name}> ----- {e.message()}"
        )
        return bh

    G = create_surface_graph_for_domain(domain)
    bh.pi2s.extend(identify_pi_twos(domain, G))
    # TODO find 2pi groups
    components = find_small_node_groups(G)
    logger.trace(f"components = {components}")

    # TODO:pi2s

    info = (domain, G)

    # large_groups = []
    # uncategorized = []H

    for comp_ in components:
        comp = list(comp_)  # TODO: can simplify this.
        size = len(comp)
        if size > 3:
            bh.large.append(comp)
        elif size == 3:
            res = handle_components(G, comp)
            # logger.debug(
            #     f"after have handled components: {[i.name_w_domain for i in res]}"
            # )
            bend = PiThree.from_surfaces(*info, *res)
            if bend.are_vectors_correct:
                bh.pi3s.append(bend)
            else:
                bh.large.append(comp)
            # todo: check if vectors are correct, if not goes to same treatment as large..
            #
        elif size == 2:
            res = handle_components(G, comp)
            res = KappaTwo.from_surfaces(*info, *res)
            bh.kappa2s.append(res)
        elif size == 1:
            res = handle_components(G, comp)[0]
            if is_part_of_pi_twos(bh.pi2s, res):
                continue

            bend = KappaOne.from_surfaces(*info, res)
            if bend.are_vectors_correct:
                bh.kappas.append(bend)
                continue

            bend = PiOne.from_surfaces(*info, res)
            if bend.are_vectors_correct:
                bh.pis.append(bend)
                continue

            bh.not_found.append(comp)

        # bh larges and bad pi3s become kappa2s
        for comp in bh.large:
            res = handle_components(G, comp)
            s1, s2, *_ = res
            bend = KappaTwo.from_surfaces(*info, s1, s2)
            bh.kappa2s.append(bend)

    return bh


# TODO: consider making the checks of the bend vectos external.. ?
