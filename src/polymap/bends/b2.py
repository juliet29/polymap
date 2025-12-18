from polymap.bends.graph import (
    create_surface_graph_for_domain,
    find_small_node_groups,
    handle_components,
)
from polymap.geometry.ortho import FancyOrthoDomain
from polymap.bends.i2 import BendHolder, KappaOne, KappaTwo, PiOne, PiThree


def assign_bends(domain: FancyOrthoDomain):
    G = create_surface_graph_for_domain(domain)
    components = find_small_node_groups(G)

    # TODO:pi2s

    info = (domain, G)
    bh = BendHolder()

    # large_groups = []
    # uncategorized = []H

    for comp_ in components:
        comp = list(comp_)
        size = len(comp)
        if size > 3:
            bh.large.append(comp)
        elif size == 3:
            res = handle_components(G, comp)
            res = PiThree.from_surfaces(*info, *res)
            bh.pi3s.append(res)
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
