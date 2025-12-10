import matplotlib.pyplot as plt
import shapely as sp

from polymap.geometry.ortho import FancyOrthoDomain
from polymap.geometry.shapely_helpers import get_coords_from_shapely_polygon
from polymap.visuals.visuals import plot_polygon


class InvalidPolygonError(Exception):
    def __init__(
        self,
        p: sp.Polygon,
        domain_name: str,
        reason: str,
        show_failing_polygon: bool = True,
    ) -> None:
        self.p = p
        self.domain_name = domain_name
        self.reason = reason

        self.message()

        if show_failing_polygon:
            self.plot()

    def message(self):
        return f"{self.domain_name} is invalid! Reason: {self.reason}"

    @property
    def domain(self):
        coords = get_coords_from_shapely_polygon(self.p)
        return FancyOrthoDomain(coords, self.domain_name)

    def plot(self):
        fig, ax = plt.subplots()
        plot_polygon(self.p, ax=ax)
        ax.set_title(f"Failing polygon: {self.domain_name}")
        plt.show()


def validate_polygon(p: sp.Polygon, domain_name: str, show_failing_polygon=False):
    if len(p.interiors) != 0:
        raise InvalidPolygonError(p, domain_name, "Num interiors != 0")
    if not p.is_valid:
        reason = sp.is_valid_reason(p)
        raise InvalidPolygonError(p, domain_name, reason, show_failing_polygon)

    coords = get_coords_from_shapely_polygon(p)
    domain = FancyOrthoDomain(coords)

    try:
        s = [i for i in domain.surfaces]
        return s
    except ValueError as e:
        raise InvalidPolygonError(
            p, domain_name, f"Zero vectors existing on polygon: {e}"
        )
