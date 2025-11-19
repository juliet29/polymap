import shapely as sp
import geom
from utils4plans.geom import Coord

from polymap.geometry.ortho import FancyOrthoDomain
from typing import NamedTuple


class HashableVector(NamedTuple):
    x: float
    y: float


def vector_to_hashable(v: geom.Vector):
    return HashableVector(v[0], v[1])  # type: ignore


def get_coords_from_shapely_polygon(p: sp.Polygon):
    return [Coord(*i) for i in p.exterior.normalize().coords]


def needs_simplifying(domain: FancyOrthoDomain):
    print(f"{len(domain.vectors)=}")
    unique_vectors = set([vector_to_hashable(i) for i in domain.vectors])
    coords = domain.coords
    print(f"{len(unique_vectors)=}")
    print(f"{len(coords)=}")
