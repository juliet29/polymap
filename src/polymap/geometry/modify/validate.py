import matplotlib.pyplot as plt
import shapely as sp

from polymap.visuals.visuals import plot_polygon


class InvalidPolygonError(Exception):
    def __init__(
        self, p: sp.Polygon, domain_name: str, reason: str, debug: bool = True
    ) -> None:
        self.p = p
        self.domain_name = domain_name
        self.reason = reason

        self.message()

        if debug:
            self.plot()

    def message(self):
        return f"{self.domain_name} is invalid! Reason: {self.reason}"

    def plot(self):
        fig, ax = plt.subplots()
        plot_polygon(self.p, ax=ax)
        ax.set_title(f"Failing polygon: {self.domain_name}")
        plt.show()


def validate_polygon(p: sp.Polygon, domain_name: str, debug=False):
    if len(p.interiors) != 0:
        raise InvalidPolygonError(p, domain_name, "Num interiors != 0")
    if not p.is_valid:
        reason = sp.is_valid_reason(p)
        raise InvalidPolygonError(p, domain_name, reason, debug)
