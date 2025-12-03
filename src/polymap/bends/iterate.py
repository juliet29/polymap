from polymap.bends.bends import (
    apply_move,
    check_zeta_intersections,
    create_zeta_bends,
    find_small_surfs,
)
from polymap.bends.points import heal_extra_points_on_domain
from polymap.geometry.ortho import FancyOrthoDomain
from copy import deepcopy
from polymap.bends.viz import DomainMoveDetails, plot_domain_iteration
from polymap.geometry.surfaces import Surface

DEBUG = True


def clean_domain(domain: FancyOrthoDomain, surfs: list[Surface]):
    zeta_bends = create_zeta_bends(surfs, domain)

    zetas, pis = check_zeta_intersections(zeta_bends)

    surfaces: list[Surface]

    if pis:
        dom2 = apply_move(pis[0].get_move)
        surfaces = pis[0].surfaces
    elif zetas:
        dom2 = apply_move(zetas[0].get_move)

        surfaces = zetas[0].surfaces
    else:
        raise Exception("No zetas or pis")

    dom3 = heal_extra_points_on_domain(dom2)
    return DomainMoveDetails(domain, dom3, surfaces)


def iterate_clean_domain(domain_: FancyOrthoDomain, layout_id: str = "", debug=DEBUG):
    N_ITER = 20
    domain = deepcopy(domain_)
    tracker: list[DomainMoveDetails] = []

    surfs = find_small_surfs(domain)
    if not surfs:
        print(f"No small surfaces for {domain.name}")
        return domain

    count = 0
    while surfs:
        move_details = clean_domain(domain, surfs)
        tracker.append(move_details)
        domain = move_details.end_domain
        surfs = find_small_surfs(domain)

        if not surfs:
            break

        count += 1
        if count > N_ITER:
            break

    if debug:
        plot_domain_iteration(tracker, layout_id)

    return domain
