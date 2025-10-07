from polymap.interfaces import CoordsType
from polymap.geometry.ortho import FancyOrthoDomain
from dataclasses import dataclass
import shapely as sp
from polymap.visuals import plot_polygon
from polymap.examples.layout import layout as sample_layout 


@dataclass
class Layout:
    domains: list[FancyOrthoDomain]

    def plot_layout(self):
        polygons = sp.MultiPolygon([i.shapely_polygon for i in self.domains])
        plot_polygon(polygons)

    def surfaces(self):
        # have all surfaces as a list.. 
        pass


def create_layout(layout: dict[str, CoordsType]):
    domains: list[FancyOrthoDomain] = []
    for k, v in layout.items():
        domain = FancyOrthoDomain.from_tuple_list(v)
        domain.set_name(k)
        domains.append(domain)

    return Layout(domains)

if __name__ == "__main__":
    layout = create_layout(sample_layout)
    layout.plot_layout()
