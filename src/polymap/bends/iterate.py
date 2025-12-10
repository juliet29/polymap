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
from polymap.geometry.modify.validate import InvalidPolygonError
from polymap.layout.interfaces import Layout
from rich import print

DEBUG = True


def determine_bend_to_fix(surfs, domain, verbose=True):
    zeta_bends = create_zeta_bends(surfs, domain)

    bend_holder = check_zeta_intersections(zeta_bends)

    if verbose:
        print(f"[bold]Bend Holder for {domain.name}")
        bend_holder.summarize()
    return bend_holder.get_next_bend()


def clean_domain(domain: FancyOrthoDomain, surfs: list[Surface], debug=DEBUG):
    bends_to_fix = determine_bend_to_fix(surfs, domain)
    print(str(bends_to_fix.get_move))
    dom2 = apply_move(bends_to_fix.get_move, debug=debug)
    surfaces = bends_to_fix.surfaces

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
        try:
            move_details = clean_domain(domain, surfs, debug=debug)
        except (NotImplementedError, InvalidPolygonError, Exception) as e:
            print(f"[red bold]Failure for {layout_id}-{domain.name}. {e}")
            attempted_fix = determine_bend_to_fix(surfs, domain, verbose=False)
            tracker.append(DomainMoveDetails(domain, domain, attempted_fix.surfaces))
            plot_domain_iteration(tracker, layout_id)
            raise Exception(e)

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


def clean_layout(layout: Layout, layout_id: str = "", debug=DEBUG):
    # TODO: do we assume the doms are ortho coming in?
    bad_domains = []
    non_balconies = list(filter(lambda x: "balcony" not in x.name, layout.domains))

    new_doms = []
    for dom in non_balconies:
        new_dom = iterate_clean_domain(dom, layout_id, False)
        if not new_dom:
            bad_domains.append(f"{layout_id}_{dom.name}")
            new_doms.append(dom)
        else:
            new_doms.append(new_dom)

    # check is ortho
    for dom in new_doms:
        assert dom.is_orthogonal, f"{dom.name} is not orthogonal"

    return Layout(new_doms), bad_domains
