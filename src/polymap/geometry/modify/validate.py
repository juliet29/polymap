import matplotlib.pyplot as plt
from typing import Literal
from polymap.layout.interfaces import Layout
from itertools import combinations
from loguru import logger
import shapely as sp

from polymap.geometry.ortho import FancyOrthoDomain
from polymap.geometry.shapely_helpers import get_coords_from_shapely_polygon
from polymap.geometry.vectors import is_perp_to_basis_vectors
from polymap.visuals.visuals import plot_polygon


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
        self, domains: list[FancyOrthoDomain], type_: Literal["INTERSECTION"]
    ) -> None:
        self.domains = domains
        self.type_ = type_

    def message(self):
        s = f"Invalid layout due to {self.type_} involving {[i.name for i in self.domains]}"
        logger.error(s)


# slow, naive check -> better check needs other graph..
def validate_layout(layout: Layout):
    combos = combinations(layout.domains, 2)
    for pair in combos:
        a, b = pair
        if a.polygon.overlaps(b.polygon):
            raise InvalidLayoutError([a, b], "INTERSECTION")

    return True
