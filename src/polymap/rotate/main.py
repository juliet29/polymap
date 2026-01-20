import shapely as sp

from polymap.geometry.ortho import FancyOrthoDomain
from polymap.geometry.shapely_helpers import get_coords_from_shapely_polygon
from polymap.geometry.layout import Layout
from polymap.rotate.utils import rotate_multipolygon
from itertools import starmap


def rotate_layout(layout: Layout):
    polygons = list(map(lambda x: x.polygon, layout.domains))
    mpol = sp.MultiPolygon(polygons)
    angle, rot_mpol = rotate_multipolygon(mpol)

    new_domains = starmap(
        lambda poly, dom: FancyOrthoDomain(
            get_coords_from_shapely_polygon(poly), name=dom.name
        ),
        zip(rot_mpol.geoms, layout.domains),
    )
    return angle, Layout(list(new_domains))
