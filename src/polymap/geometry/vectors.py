import shapely as sp
from utils4plans.geom import Coord
from utils4plans.lists import get_unique_one
import geom
from enum import Enum
from dataclasses import dataclass
from typing import Literal, Iterable
from typing import TypeVar, Callable
import numpy as np

T = TypeVar("T")


Axes = Literal["X", "Y"]


class BasisVectors:
    e0 = geom.Vector([1, 0, 0])
    e1 = geom.Vector([0, 1, 0])
    e2 = geom.Vector([0, 0, 1])


DirectionNames = Literal["north", "south", "east", "west"]


@dataclass
class Direction:
    name: DirectionNames
    aligned_axis: Axes
    aligned_vector: geom.Vector

    def match_vector(self, v: geom.Vector):
        if v == self.aligned_vector:
            return self

    @property
    def normal_axis(self):
        if self.aligned_axis == "X":
            return "Y"
        return "X"

    def __lt__(self, other):
        if isinstance(other, Direction):
            return self.name < other.name


class CardinalDirections:
    NORTH = Direction("north", "Y", BasisVectors.e1)
    SOUTH = Direction("south", "Y", -1 * BasisVectors.e1)
    EAST = Direction("east", "X", BasisVectors.e0)
    WEST = Direction("west", "X", -1 * BasisVectors.e0)

    @property
    def drn_list(self):
        return [self.NORTH, self.SOUTH, self.EAST, self.WEST]

    def get_drn_by_vector(self, v_: geom.Vector):
        v = v_.norm()
        matches = [i.match_vector(v) for i in self.drn_list]
        try:
            res = get_unique_one(matches, lambda x: x)
            return res
        except AssertionError:
            raise Exception(f"{v} has 0 or many potential matches: {matches}")


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
    if v.dot(BasisVectors.e0) == 0 or v.dot(BasisVectors.e1) == 0:
        return True
    return False


def is_near_perp_to_basis_vectors(v: geom.Vector):
    # TODO assert is 3D
    if np.isclose(v.dot(BasisVectors.e0), 0) or np.isclose(v.dot(BasisVectors.e1), 0):
        return True
    return False


def compute_outward_normal_assuming_cw(v_: geom.Vector):
    v = v_.norm()
    assert is_perp_to_basis_vectors(v)

    cross_prod = BasisVectors.e2.cross(v)

    return cross_prod


def determine_normal_direction(v: geom.Vector):
    normal_vector = compute_outward_normal_assuming_cw(v)
    return CardinalDirections().get_drn_by_vector(normal_vector)


def sp_line_to_vector(line: sp.LineString):
    coords = [Coord(*i) for i in line.coords]
    return vector_from_coords(*coords, _2D=False)


def vector_to_sp_line(v: geom.Vector):
    if len(v) == 3:
        assert v[2] == 0

    end_coord = (float(v[0]), float(v[1]))  # type: ignore
    return sp.LineString([(0, 0), end_coord])
