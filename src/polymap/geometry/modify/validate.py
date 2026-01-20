import matplotlib.pyplot as plt
import numpy as np
from typing import Literal

from rich.pretty import pretty_repr
from polymap.config import OVERLAP_TOLERANCE
from polymap.geometry.layout import Layout
from itertools import combinations
from loguru import logger
import shapely as sp

from polymap.geometry.ortho import FancyOrthoDomain
from polymap.geometry.shapely_helpers import get_coords_from_shapely_polygon
from polymap.geometry.vectors import is_perp_to_basis_vectors
from polymap.visuals.visuals import plot_layout_alone, plot_polygon
from utils4plans.geom import ShapelyBounds


class InvalidPolygonError(Exception):
    def __init__(
        self,
        p: sp.Polygon,
        domain_name: str,
        reason: str,
        show_failing_polygon: bool = False,
    ) -> None:
        self.p = p
        self.domain_name = domain_name
        self.reason = reason

        self.message()

        if show_failing_polygon:
            self.plot()

    def message(self):
        logger.error(
            f"[italic orange]{self.domain_name} is invalid! Reason: {self.reason}"
        )

    @property
    def domain(self):
        coords = get_coords_from_shapely_polygon(self.p)
        return FancyOrthoDomain(coords, self.domain_name)

    def plot(self):
        fig, ax = plt.subplots()
        plot_polygon(self.p, ax=ax)
        ax.set_title(f"Failing polygon: {self.domain_name}")
        plt.show()


def validate_polygon(p: sp.Polygon, domain_name: str):
    if len(p.interiors) != 0:
        raise InvalidPolygonError(p, domain_name, "Num interiors != 0")
    if not p.is_valid:
        reason = sp.is_valid_reason(p)
        raise InvalidPolygonError(p, domain_name, reason)

    coords = get_coords_from_shapely_polygon(p)
    domain = FancyOrthoDomain(coords)

    # check for zero vectors..
    for v, coords in zip(domain.vectors, domain.paired_coords):
        try:
            assert v.mag() != 0
        except AssertionError:
            raise InvalidPolygonError(
                p, domain_name, f"Zero vector existing near {str(coords)}: v={v}"
            )
        try:
            assert is_perp_to_basis_vectors(v)
        except AssertionError:
            raise InvalidPolygonError(
                p, domain_name, f"Non-ortho vector near {str(coords)}: v={v}"
            )


class InvalidLayoutError(Exception):
    def __init__(
        self,
        domains: list[FancyOrthoDomain],
        type_: Literal["INTERSECTION"],
        layout: Layout,
    ) -> None:
        self.domains = domains
        self.type_ = type_
        self.layout = layout

    @property
    def overlap(self):
        a = self.domains[0]
        b = self.domains[1]
        overlap = sp.intersection(a.polygon, b.polygon)
        return overlap

    def message(self):
        s = f"Invalid layout due to {self.type_} involving {[i.name for i in self.domains]}"
        logger.error(s)

    def plot(self):
        plot_layout_alone(
            self.layout, show_surface_labels=True, layout_name="Failing Layout"
        )
        plot_polygon(
            self.overlap,  # pyright: ignore[reportArgumentType]
            title=f"Intersection of {self.domains[0].name} and {self.domains[1].name}",
        )
        logger.debug(
            f"Overlap is {type(self.overlap)} and has bounds {pretty_repr(self.overlap.bounds)}"
        )
        plt.show()


def overlap_near_zero(
    domains: tuple[FancyOrthoDomain, FancyOrthoDomain], tolerance=OVERLAP_TOLERANCE
):
    a, b = domains
    overlap = sp.intersection(a.polygon, b.polygon)

    area_near_zero = np.isclose(overlap.area, 0)
    logger.debug(f"overlap area between {a.name}, {b.name}: {overlap.area}")
    if area_near_zero:
        return True
    bounds = ShapelyBounds(*overlap.bounds)
    xsz = bounds.domain.horz_range.size()
    x_near_zero = np.isclose(xsz, 0)

    ysz = bounds.domain.vert_range.size()
    y_near_zero = np.isclose(ysz, 0)

    if x_near_zero or y_near_zero:
        return True


# slow, naive check -> better check needs other graph..
def validate_layout_after_move(
    layout: Layout, a: FancyOrthoDomain, b: FancyOrthoDomain
):
    # logger.info(f"{a.name, b.name}")

    if a.polygon.overlaps(b.polygon):
        logger.warning(f"{a.name} overlaps {b.name}")
        if overlap_near_zero((a, b)):
            pass
        raise InvalidLayoutError([a, b], "INTERSECTION", layout)

    return True


def validate_layout_overlaps(layout: Layout):
    combos = list(combinations(layout.domains, 2))

    overlaps = []
    for pair in combos:
        a, b = pair
        if a.polygon.overlaps(b.polygon):
            if overlap_near_zero((a, b)):
                overlaps.append((a.name, b.name))
                continue
            raise InvalidLayoutError([a, b], "INTERSECTION", layout)

    # if domain and overlaps:
    #     logger.warning(
    #         f"overlaps surrounding domain [bold]{domain.name}[/bold]: {pretty_repr(overlaps)}"
    #     )
    # elif not domain:
    if overlaps:
        logger.critical(
            f"{len(overlaps)} NEAR ZERO OVERLAPS ACROSS THE LAYOUT! {pretty_repr(overlaps)}"
        )
    else:
        logger.success("No overlaps in the layout")


def validate_layout_no_holes(layout: Layout):
    # union and check for holes

    all_polys = [dom.polygon for dom in layout.domains]
    union_poly = sp.union_all(all_polys)
    num_holes = sp.get_num_interior_rings(union_poly)
    return num_holes
