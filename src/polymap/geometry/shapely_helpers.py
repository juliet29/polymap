import shapely as sp
from utils4plans.geom import Coord

from polymap.config import PRECISION


def decrease_precision(polygon: sp.Polygon, precision: int = PRECISION):
    return sp.from_wkt(sp.to_wkt(polygon, rounding_precision=precision))


def get_coords_from_shapely_geom(geom: sp.Point | sp.LineString):
    coords = geom.coords
    return [Coord(*i) for i in coords]


def get_coords_from_shapely_polygon(p: sp.Polygon):
    return [Coord(*i) for i in p.exterior.normalize().coords]
