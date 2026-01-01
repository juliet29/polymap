from polymap.bends.b2 import assign_bends
from polymap.examples.msd import MSDDomain
from polymap.geometry.ortho import FancyOrthoDomain

from polymap.bends.utils import (
    apply_move,
    find_small_surfs,
)
from polymap.bends.i2 import Bend, BendHolder
from polymap.bends.points import heal_extra_points_on_domain
from copy import deepcopy
from polymap.bends.viz import DomainMoveDetails, plot_domain_iteration
from polymap.geometry.surfaces import Surface
from polymap.geometry.modify.validate import InvalidPolygonError, validate_polygon
from typing import Literal

from loguru import logger

FAIL_TYPES = Literal[
    "Invalid Move",
    "Problem Finding Bends",
    "Failed to Clean Domain Correctly",
    "Invalid Incoming Domain",
    "Exceeded number of iterations",
]


class DomainCleanFailure(Exception):
    def __init__(
        self,
        domain: FancyOrthoDomain,
        fail_type: FAIL_TYPES,
        details: str,
        surfaces: list[Surface] = [],
        bends: BendHolder | None = None,
        current_bend: Bend | None = None,
    ):
        self.domain = domain
        self.fail_type = fail_type
        self.details = details
        self.surfaces = surfaces
        self.bends = bends
        self.current_bend = current_bend

    def __rich_repr__(self):
        yield "domain", self.domain.name
        yield "fail_type", self.fail_type
        yield "details", self.details

    def show_message(self, layout_id: str):
        logger.warning(f"[red bold]{self.fail_type} for {layout_id}-{self.domain.name}")
        logger.warning(f"{self.details}")

        if self.bends:
            logger.warning(self.bends.summary_str)

        if self.current_bend:
            logger.warning(f"Current bend is {str(self.current_bend)}")
            logger.warning(self.current_bend.study_vectors())


class DomainCleanIterationFailure(Exception):
    def __init__(
        self, domain_name: str, fail_type: FAIL_TYPES, current_bend: Bend | None = None
    ):
        self.domain = domain_name
        self.fail_type = fail_type
        self.current_bend = current_bend

    def message(self):
        logger.warning(f"[red bold]{self.fail_type} for {self.domain}")


def clean_domain(domain: FancyOrthoDomain, domain_name: str = ""):
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
        logger.info(f"No small surfaces for {domain_name}. Ending iteration...")
        return domain

    logger.info(f"[blue italic]Starting iteration for {domain_name}")
    count = 0
    while small_surfs:

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

    logger.info(f"[green italic]Successfully completed iteration for {domain_name}")

    return domain
