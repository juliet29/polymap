from polymap.bends.bends import (
    ProblemIdentifyingBend,
    apply_move,
    check_eta_intersections,
    create_eta_bends,
    find_small_surfs,
    show_problem_bends,
)
from polymap.bends.interfaces import Bend
from polymap.bends.points import heal_extra_points_on_domain
from polymap.geometry.ortho import FancyOrthoDomain
from copy import deepcopy
from polymap.bends.viz import DomainMoveDetails, plot_domain_iteration
from polymap.geometry.surfaces import Surface
from polymap.geometry.modify.validate import InvalidPolygonError, validate_polygon
from polymap.layout.interfaces import Layout
from rich import print
from typing import Literal

DEBUG = True


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


def determine_bend_to_fix(surfs, domain, verbose=True):
    zeta_bends = create_eta_bends(surfs, domain)

    bend_holder = check_eta_intersections(zeta_bends)

    if verbose:
        bend_holder.summarize()
    return bend_holder.get_next_bend()


def clean_domain(domain: FancyOrthoDomain, surfs: list[Surface]):

    try:
        bends_to_fix = determine_bend_to_fix(surfs, domain)
    except ProblemIdentifyingBend as e:
        raise DomainCleanFailure(
            domain, "Problem Finding Bends", e.reason, bends=e.bends
        )

    try:
        dom2 = apply_move(bends_to_fix.get_move)
    except InvalidPolygonError as e:
        raise DomainCleanFailure(
            e.domain, "Invalid Move", e.reason, surfaces=bends_to_fix.surfaces
        )

    try:
        dom3 = heal_extra_points_on_domain(dom2)
    except InvalidPolygonError as e:
        raise DomainCleanFailure(
            e.domain,
            "Failed to Clean Domain Correctly",
            e.reason,
            surfaces=bends_to_fix.surfaces,
        )
    return DomainMoveDetails(domain, dom3, bends_to_fix.surfaces)


def iterate_clean_domain(
    domain_: FancyOrthoDomain,
    layout_id: str = "",
    show_complete_iteration=False,
    show_failure: bool = False,
):
    N_ITER = 20
    domain = deepcopy(domain_)
    tracker: list[DomainMoveDetails] = []

    try:
        validate_polygon(domain.polygon, domain.name)
    except InvalidPolygonError as e:
        print(
            f"Coukd not clean {domain.name} because incoming polygon is invalid. {e.reason}"
        )
        if show_failure:
            tracker.append(DomainMoveDetails(domain, domain, []))
            plot_domain_iteration(tracker, layout_id)
        raise DomainCleanFailureReport(domain.name, "Invalid incoming domain")

    surfs = find_small_surfs(domain)
    if not surfs:
        print(f"No small surfaces for {domain.name}")
        return domain

    print(f"[blue italic]Starting iteration for {domain.name}")

    count = 0
    while surfs:
        try:
            move_details = clean_domain(domain, surfs)
        except DomainCleanFailure as e:
            e.show_message(layout_id)
            if show_failure:
                tracker.append(
                    DomainMoveDetails(
                        domain, e.domain, e.surfaces, show_second_surf=False
                    )
                )
                plot_domain_iteration(tracker, layout_id)
            raise DomainCleanFailureReport(domain.name, e.fail_type)

        tracker.append(move_details)
        domain = move_details.end_domain

        surfs = find_small_surfs(domain)

        if not surfs:
            break

        count += 1
        if count > N_ITER:
            raise DomainCleanFailureReport(
                domain.name, f"Exceeded number of iterations={N_ITER}"
            )

    if show_complete_iteration:
        plot_domain_iteration(tracker, layout_id)

    print(f"[green italic]Successfully completed iteration for {domain.name}")

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
