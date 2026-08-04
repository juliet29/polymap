import shapely
from loguru import logger

from polyfix.geometry.layout import Layout
from polyfix.geometry.modify.validate import validate_polygon
from polyfix.geometry.ortho import FancyOrthoDomain
from polyfix.geometry.shapely_helpers import get_coords_from_shapely_polygon
from polyfix.reconcile.hole_finder import HoleFinder


def update_domain_and_layout(
    layout: Layout, new_geom: shapely.Polygon, original_domain: FancyOrthoDomain
):
    pass
    validate_polygon(new_geom, original_domain.name)
    new_domain = FancyOrthoDomain(
        get_coords_from_shapely_polygon(new_geom), name=original_domain.name
    )
    new_layout = Layout(
        [new_domain if d.name == original_domain.name else d for d in layout.domains]
    )
    return new_layout


def reconcile_one(hf: HoleFinder, hole: shapely.Polygon):
    layout = hf.layout
    possible_geoms = hf.tree.query(hole, "touches")
    geom_ix = possible_geoms[0]
    domain = layout.domains[geom_ix]
    union = shapely.unary_union(shapely.MultiPolygon([domain.polygon, hole]))
    assert isinstance(union, shapely.Polygon)
    return update_domain_and_layout(layout, union, domain)


def reconcile_all(layout: Layout, max_iter: int = 10):
    for iteration in range(max_iter):
        hf = HoleFinder(layout)
        holes = hf.holes_list
        if not holes:
            logger.success("We are done hole finding")
            return layout
        logger.info(f"Adressing holes - iter {iteration}")
        layout = reconcile_one(hf, holes[0])
    raise RuntimeError(f"holes remain after max_iter={max_iter}")
