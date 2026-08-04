from dataclasses import dataclass

import shapely
from matplotlib.figure import Figure

from polyfix.geometry.layout import Layout
from polyfix.geometry.modify.validate import validate_polygon
from polyfix.geometry.ortho import FancyOrthoDomain
from polyfix.geometry.shapely_helpers import get_coords_from_shapely_polygon
from polyfix.reconcile.viz import (
    plot_domain_hole_union,
    plot_hole_finder,
)


@dataclass
class HoleFinder:
    layout: Layout

    @property
    def geoms(self) -> shapely.MultiPolygon:
        return shapely.MultiPolygon([i.polygon for i in self.layout.domains])

    @property
    def union(self):
        return shapely.unary_union(self.geoms)

    @property
    def interiors(self) -> shapely.MultiPolygon:
        return shapely.MultiPolygon(
            [
                shapely.Polygon(ring)
                for part in shapely.get_parts(self.union)
                if isinstance(part, shapely.Polygon)
                for ring in part.interiors
            ]
        )

    @property
    def holes_list(self):
        return list(shapely.get_parts(self.interiors))

    @property
    def tree(self):
        return shapely.STRtree(shapely.get_parts(self.geoms))

    def plot(self) -> Figure:
        return plot_hole_finder(self.geoms, self.union, self.interiors)


def study_replace_domain_with_hole(
    layout: Layout, tree: shapely.STRtree, hole: shapely.Polygon
):
    possible_geoms = tree.query(hole, "touches")
    geom_ix = possible_geoms[0]

    domain = layout.domains[geom_ix]
    union = shapely.unary_union(shapely.MultiPolygon([domain.polygon, hole]))
    return plot_domain_hole_union(domain.polygon, hole, union)



