from polymap.bends.b2 import assign_bends
from polymap.examples.msd import MSDDomain
from polymap.geometry.ortho import FancyOrthoDomain

from polymap.bends.bends import (
    apply_move,
    find_small_surfs,
    show_problem_bends,
)
from polymap.bends.interfaces import Bend
from polymap.bends.points import heal_extra_points_on_domain
from copy import deepcopy
from polymap.bends.viz import DomainMoveDetails, plot_domain_iteration
from polymap.geometry.surfaces import Surface
from polymap.geometry.modify.validate import InvalidPolygonError, validate_polygon
from rich import print
from typing import Literal

from loguru import logger

FAIL_TYPES = Literal[
    "Invalid Move", "Problem Finding Bends", "Failed to Clean Domain Correctly"
]


class DomainCleanFailure(Exception):
    def __init__(
        self,
        domain: FancyOrthoDomain,
        fail_type: FAIL_TYPES,
        details: str,
        surfaces: list[Surface] = [],
        bends: list[Bend] = [],
    ):
        self.domain = domain
        self.fail_type = fail_type
        self.details = details
        self.surfaces = surfaces
        self.bends = bends

    def __rich_repr__(self):
        yield "domain", self.domain.name
        yield "fail_type", self.fail_type
        yield "details", self.details

    def show_message(self, layout_id: str):
        print(f"[red bold]{self.fail_type} for {layout_id}-{self.domain.name}")
        print(f"[red]{self.details}")

        if self.bends:
            show_problem_bends(self.bends)


class DomainCleanFailureReport(Exception):
    def __init__(
        self,
        domain_name: str,
        fail_type: str,
    ):
        self.domain = domain_name
        self.fail_type = fail_type

    def message(self):
        print(f"[red bold]{self.fail_type} for {self.domain}")


def clean_domain(domain: FancyOrthoDomain, domain_name: str = ""):
    try:
        bend_holder = assign_bends(domain, domain_name)
    except:
        raise Exception

    current_bend = bend_holder.get_next_bend()
    try:
        dom2 = apply_move(current_bend.get_move)
    except InvalidPolygonError as e:
        raise DomainCleanFailure(
            e.domain, "Invalid Move", e.reason, surfaces=current_bend.surfaces
        )

    try:
        dom3 = heal_extra_points_on_domain(dom2)
    except InvalidPolygonError as e:
        raise DomainCleanFailure(
            e.domain,
            "Failed to Clean Domain Correctly",
            e.reason,
            surfaces=current_bend.surfaces,
        )
    return DomainMoveDetails(domain, dom3, current_bend.surfaces)


def iterate_clean_domain(
    msd_domain: MSDDomain,
    show_complete_iteration=False,
    show_failure: bool = False,
):
    N_ITER = 20
    domain = deepcopy(msd_domain.domain)

    layout_id = msd_domain.name.layout_id
    domain_name = msd_domain.name.display_name
    tracker: list[DomainMoveDetails] = []

    try:
        validate_polygon(domain.polygon, domain_name)
    except InvalidPolygonError as e:
        logger.error(
            f"Could not clean {domain_name} because incoming polygon is invalid. {e.reason}"
        )
        if show_failure:
            tracker.append(DomainMoveDetails(domain, domain, []))
            plot_domain_iteration(tracker, layout_id)
        raise DomainCleanFailureReport(domain_name, "Invalid incoming domain")

    small_surfs = find_small_surfs(domain)
    if not small_surfs:
        logger.success(f"No small surfaces for {domain_name}")
        return domain

    count = 0
    while small_surfs:
        logger.info(f"[blue italic]Starting iteration for {domain_name}")

        if len(domain.surfaces) <= 4:
            break

        try:
            move_details = clean_domain(domain, msd_domain.name.display_name)
        except DomainCleanFailure as e:
            e.show_message(layout_id)
            if show_failure:
                tracker.append(
                    DomainMoveDetails(
                        domain, e.domain, e.surfaces, show_second_surf=False
                    )
                )
                plot_domain_iteration(tracker, layout_id)
            raise DomainCleanFailureReport(msd_domain.name.display_name, e.fail_type)

        tracker.append(move_details)
        domain = move_details.end_domain

        small_surfs = find_small_surfs(domain)

        if not small_surfs:
            break

        count += 1
        if count > N_ITER:
            raise DomainCleanFailureReport(
                f"{layout_id}-{domain.name}", f"Exceeded number of iterations={N_ITER}"
            )

    if show_complete_iteration:
        plot_domain_iteration(tracker, layout_id)

    logger.success(f"[green italic]Successfully completed iteration for {domain_name}")

    return domain
