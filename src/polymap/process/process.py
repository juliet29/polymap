from polymap.geometry.ortho import FancyOrthoDomain
from polymap.geometry.shapely_helpers import get_coords_from_shapely_polygon
from polymap.layout.interfaces import Layout
from polymap.nonortho.dot import make_ortho_coords
import shapely as sp

TOLERANCE = 0.15


def simplify_layout(layout: Layout, tolerance: float = TOLERANCE):
    def simplify_domain(dom: FancyOrthoDomain):
        simple_poly = sp.simplify(dom.polygon, tolerance=tolerance)
        simple_dom = FancyOrthoDomain(get_coords_from_shapely_polygon(simple_poly))

        ortho_coords = make_ortho_coords(simple_dom.coords, simple_dom.vectors)

        ortho_dom = FancyOrthoDomain(ortho_coords, dom.name)
        return ortho_dom

    new_doms = [simplify_domain(i) for i in layout.domains]
    return Layout(new_doms)
