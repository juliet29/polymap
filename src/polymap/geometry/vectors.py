import shapely as sp
from utils4plans.geom import Coord
from utils4plans.lists import get_unique_one
import geom
from dataclasses import dataclass
from typing import Literal, get_args
from typing import TypeVar
import numpy as np

T = TypeVar("T")


Axes = Literal["X", "Y"]

VectorComponents = Literal["x", "y", "z"]


class BasisVectors:
    e0 = geom.Vector([1, 0, 0])
    e1 = geom.Vector([0, 1, 0])
    e2 = geom.Vector([0, 0, 1])


BaseVectorNames = Literal["e0", "e1", "n_e0", "n_e1"]


class BasisVectors2D:
    e0 = geom.Vector([1, 0, 0])
    e1 = geom.Vector([0, 1, 0])
    vectors = [e0, e1, -e0, -e1]
    vector_names: list[BaseVectorNames] = ["e0", "e1", "n_e0", "n_e1"]


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

    @property
    def positive_vector(self):
        if self.aligned_vector.x < 0 or self.aligned_vector.y < 0:  # type: ignore
            # TODO: use get compoenent function..
            return -1 * self.aligned_vector
        return self.aligned_vector

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


def get_component(v: geom.Vector, comp: VectorComponents):
    try:
        return v.__getattribute__(comp)
    except (ValueError, AttributeError, KeyError):
        return 0


def vector2D_from_coord(c: Coord):
    return geom.Vector(c.as_tuple)


def vector_from_coords(c1: Coord, c2: Coord, _2D=False):
    if _2D:
        v1, v2 = [vector2D_from_coord(i) for i in [c1, c2]]
    else:
        v1, v2 = [vector3D_from_coord(i) for i in [c1, c2]]
    v = v2 - v1
    true_x, true_y = (
        v.x,
        v.y,
    )
    if np.isclose(get_component(v, "x"), 0):
        true_x = 0
    if np.isclose(get_component(v, "y"), 0):
        true_y = 0
    if _2D:
        return geom.Vector([true_x, true_y])

    return geom.Vector([true_x, true_y, v.z])


def vector3D_from_coord(c: Coord):
    return geom.Vector([*c.as_tuple, 0])


def is_perpendicular(v1: geom.Vector, v2: geom.Vector):
    return v1.dot(v2) == 0


def is_perp_to_basis_vectors(v: geom.Vector):
    # TODO assert is 3D
    if is_perpendicular(v, BasisVectors.e0) or is_perpendicular(v, BasisVectors.e1):
        return True
    return False


def is_near_perpendicular(v1: geom.Vector, v2: geom.Vector):
    return np.isclose(v1.dot(v2), 0)


def is_near_perp_to_basis_vectors(v: geom.Vector):
    if is_near_perpendicular(v, BasisVectors.e0) or is_near_perpendicular(
        v, BasisVectors.e1
    ):
        return True
    return False


def compute_outward_normal_assuming_cw(v_: geom.Vector):
    v = v_.norm()
    assert is_perp_to_basis_vectors(v)

    cross_prod = BasisVectors.e2.cross(v)

    return cross_prod


def get_normal_vector_assuming_cw(drn: DirectionNames):
    match drn:
        case "north":
            return CardinalDirections.EAST.aligned_vector
        case "east":
            return CardinalDirections.SOUTH.aligned_vector
        case "south":
            return CardinalDirections.WEST.aligned_vector
        case "west":
            return CardinalDirections.NORTH.aligned_vector
        # case _
        #     raise KeyError(f"Unexpected input. Wanted a member of `DirectionNames`, but got {drn}")


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


def vector_as_coord(v: geom.Vector):
    return Coord(float(v[0]), float(v[1]))  # type: ignore


def make_vector_2D(v: geom.Vector):
    if len(v) == 3:
        assert v[2] == 0
    return geom.Vector([v[0], v[1]])


def pretty_print_vector(v: geom.Vector):
    def print_component(f: float):
        if f == 0:
            return "0"
        else:
            return f"{f:.2f}"

    comps = map(
        lambda x: print_component(get_component(v, x)), get_args(VectorComponents)
    )
    x, y, z = comps
    res = f"[{x}, {y}, {z}]"
    return res
