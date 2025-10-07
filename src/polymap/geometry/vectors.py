from utils4plans.geom import Coord
import geom
from enum import Enum


class BasisVectors:
    e0 = geom.Vector([1, 0, 0])
    e1 = geom.Vector([0, 1, 0])


def vector2D_from_coord(c: Coord):
    return geom.Vector(c.as_tuple)


def vector_from_coords(c1: Coord, c2: Coord, _2D=False):
    if _2D:
        v1, v2 = [vector2D_from_coord(i) for i in [c1, c2]]
    else:
        v1, v2 = [vector3D_from_coord(i) for i in [c1, c2]]
    return v2 - v1


def vector3D_from_coord(c: Coord):
    return geom.Vector([*c.as_tuple, 0])


def is_perp_to_basis_vectors(v: geom.Vector):
    # TODO assert is 3D
    assert v.dot(BasisVectors.e0) == 0 or v.dot(BasisVectors.e1) == 0, f"{v} is not orthogonal to the basis vectors!"
    return True
