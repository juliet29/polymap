import shapely as sp
from utils4plans.geom import Coord

from polymap.config import PRECISION


def decrease_precision(polygon: sp.Polygon, precision: int = PRECISION):
    return sp.from_wkt(sp.to_wkt(polygon, rounding_precision=precision))


# class HashableVector(NamedTuple):
#     x: float
#     y: float
#
#
def get_coords_from_shapely_geom(geom: sp.Point | sp.LineString):
    coords = geom.coords
    return [Coord(*i) for i in coords]


#
# def vector_to_hashable(v: geom.Vector):
#     return HashableVector(v[0], v[1])  # type: ignore
#
#
def get_coords_from_shapely_polygon(p: sp.Polygon):
    return [Coord(*i) for i in p.exterior.normalize().coords]


#
#
# def needs_simplifying(domain: FancyOrthoDomain):
#     print(f"{len(domain.vectors)=}")
#     unique_vectors = set([vector_to_hashable(i) for i in domain.vectors])
#     coords = domain.coords
#     print(f"{len(unique_vectors)=}")
#     print(f"{len(coords)=}")
