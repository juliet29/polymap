from loguru import logger
from polymap.geometry.modify.validate import InvalidPolygonError, validate_polygon
from polymap.bends.graph import (
    create_surface_graph_for_domain,
    find_small_node_groups,
    handle_components,
)
from polymap.geometry.ortho import FancyOrthoDomain
from polymap.bends.i2 import BendHolder, KappaOne, KappaTwo, PiOne, PiThree


def assign_bends(domain: FancyOrthoDomain):

    bh = BendHolder()
    try:
        validate_polygon(domain.polygon, domain.name)
    except InvalidPolygonError as e:
        logger.error(
            f"Could not validate polygon, and could not assign bends ----- {e.message()}"
        )
        return bh

    G = create_surface_graph_for_domain(domain)
    # TODO find 2pi groups
    components = find_small_node_groups(G)
    logger.trace(f"components = {components}")

    # TODO:pi2s

    info = (domain, G)

    # large_groups = []
    # uncategorized = []H

    for comp_ in components:
        comp = list(comp_)  # TODO: can fix this.
        size = len(comp)
        if size > 3:
            bh.large.append(comp)
        elif size == 3:
            res = handle_components(G, comp)
            logger.debug(
                f"after have handled components: {[i.name_w_domain for i in res]}"
            )
            res = PiThree.from_surfaces(*info, *res)
            bh.pi3s.append(res)
            # todo: check if vectors are correct, if not goes to same treatment as large..
            #
        elif size == 2:
            res = handle_components(G, comp)
            res = KappaTwo.from_surfaces(*info, *res)
            bh.kappa2s.append(res)
        elif size == 1:
            res = handle_components(G, comp)[0]
            bend = KappaOne.from_surfaces(*info, res)
            if bend.are_vectors_correct:
                bh.kappas.append(bend)
                continue

            bend = PiOne.from_surfaces(*info, res)
            if bend.are_vectors_correct:
                bh.pis.append(bend)
                continue

            bh.not_found.append(comp)

    return bh


# TODO: consider making the checks of the bend vectos external.. ?
