from polymap.bends.bends import assign_bends
from polymap.examples.msd import MSDDomain, MSDDomainName
from polymap.geometry.ortho import FancyOrthoDomain

from polymap.bends.utils import (
    apply_move,
    find_small_surfs,
)
from polymap.bends.points import heal_extra_points_on_domain
from copy import deepcopy
from polymap.bends.viz import DomainMoveDetails, plot_domain_iteration
from polymap.geometry.modify.validate import InvalidPolygonError, validate_polygon
from polymap.bends.errors import DomainCleanFailure, DomainCleanIterationFailure

from loguru import logger

from polymap.geometry.layout import Layout


def remove_one_bend_from_domain(domain: FancyOrthoDomain, domain_name: str = ""):
    bend_holder = assign_bends(domain, domain_name)

    current_bend = bend_holder.get_next_bend()
    try:
        dom2 = apply_move(current_bend.get_move)
    except InvalidPolygonError as e:
        raise DomainCleanFailure(
            e.domain,
            "Invalid Move",
            e.reason,
            surfaces=current_bend.surfaces,
            bends=bend_holder,
            current_bend=current_bend,
        )

    try:
        dom3 = heal_extra_points_on_domain(dom2)
    except InvalidPolygonError as e:
        raise DomainCleanFailure(
            e.domain,
            "Failed to Clean Domain Correctly",
            e.reason,
            surfaces=current_bend.surfaces,
            current_bend=current_bend,
        )
    return DomainMoveDetails(domain, dom3, current_bend.surfaces)


def remove_all_bends_from_domain(
    msd_domain: MSDDomain,
    show_complete_iteration=False,
    show_failure: bool = False,
):
    N_ITER = 20
    domain = deepcopy(msd_domain.domain)

    layout_id = msd_domain.name.layout_id
    domain_name = msd_domain.name.display_name
    tracker: list[DomainMoveDetails] = []

    logger.info(f"[blue italic]Starting to clean {domain_name}")

    try:
        validate_polygon(domain.polygon, domain_name)
    except InvalidPolygonError as e:
        # TODO: this is redundant and could be cleaned up..
        logger.warning(
            f"Could not clean {domain_name} because incoming polygon is invalid. {e.reason}"
        )
        if show_failure:
            tracker.append(DomainMoveDetails(domain, domain, []))
            plot_domain_iteration(tracker, layout_id)
        raise DomainCleanIterationFailure(domain_name, "Invalid Incoming Domain")

    small_surfs = find_small_surfs(domain)
    if not small_surfs:
        logger.info(f"No small surfaces for {domain_name}. Ending iteration...\n")
        return domain

    logger.info(f"[blue italic]Starting iteration for {domain_name}")
    count = 0
    while small_surfs:

        if len(domain.surfaces) <= 4:
            break

        try:
            move_details = remove_one_bend_from_domain(
                domain, msd_domain.name.display_name
            )
        except DomainCleanFailure as e:
            e.show_message(layout_id)
            if show_failure:
                tracker.append(
                    DomainMoveDetails(
                        domain, e.domain, e.surfaces, show_second_surf=False
                    )
                )
                plot_domain_iteration(tracker, layout_id)
            raise DomainCleanIterationFailure(
                msd_domain.name.display_name,
                e.fail_type,  # pyright: ignore[reportArgumentType]
                current_bend=e.current_bend,
            )

        tracker.append(move_details)
        domain = move_details.end_domain

        small_surfs = find_small_surfs(domain)

        if not small_surfs:
            break

        count += 1
        if count > N_ITER:
            raise DomainCleanIterationFailure(
                f"{domain_name}", "Exceeded number of iterations"
            )

    if show_complete_iteration:
        plot_domain_iteration(tracker, layout_id)

    logger.info(f"[green italic]Successfully completed iteration for {domain_name}\n")

    return domain


def remove_bends_from_layout(layout: Layout, layout_id: str = ""):
    # TODO: do we assume the doms are ortho coming in?
    bad_domains = []
    non_balconies = list(filter(lambda x: "balcony" not in x.name, layout.domains))

    new_doms = []
    for dom in layout.domains:
        try:
            msd_dom = MSDDomain(MSDDomainName(layout_id, dom.name), dom)
            new_dom = remove_all_bends_from_domain(msd_dom)
            new_doms.append(new_dom)
        except DomainCleanIterationFailure as e:
            bad_domains.append(f"{e.domain}")
            new_doms.append(dom)

    # check is ortho
    for dom in new_doms:
        assert dom.is_orthogonal, f"{dom.name} is not orthogonal"

    return Layout(new_doms), bad_domains
