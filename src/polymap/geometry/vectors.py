from utils4plans.geom import Coord
import geom
from enum import Enum
from dataclasses import dataclass
from typing import Literal

# class Axes: # TODO literal?
#     X = "X"
# Y = "Y"
Axes = Literal["X", "Y"]


class BasisVectors:
    e0 = geom.Vector([1, 0, 0])
    e1 = geom.Vector([0, 1, 0])
    e2 = geom.Vector([0, 0, 1])


@dataclass
class Direction:
    name: str
    aligned_axis: Axes
    aligned_vector: geom.Vector

    def match_vector(self, v: geom.Vector):
        if v == self.aligned_vector:
            return self


class CardinalDirections:
    NORTH = Direction("north", "Y", BasisVectors.e1)
    SOUTH = Direction("south", "Y", -1 * BasisVectors.e1)
    EAST = Direction("east", "X", BasisVectors.e0)
    WEST = Direction("west", "X", -1 * BasisVectors.e0)

    @property
    def drn_list(self):
        return [self.NORTH, self.SOUTH, self.EAST, self.WEST]

    # @property
    # def drn_by_vector(self):
    #     return {i.aligned_vector: i for i in self.drn_list}

    def get_drn_by_vector(self, v: geom.Vector):
        matches = [i.match_vector(v) for i in self.drn_list]
        valid_matches = [i for i in matches if i]
        assert len(valid_matches) == 1
        return valid_matches[0]


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
    assert v.dot(BasisVectors.e0) == 0 or v.dot(BasisVectors.e1) == 0, (
        f"{v} is not orthogonal to the basis vectors!"
    )
    return True


# def is_parallel(v: geom.Vector, test_vector: geom.Vector):
#     if v.dot(test_vector) == 1 or v.dot(test_vector) == -1:
#         return True


def compute_outward_normal_assuming_cw(v_: geom.Vector):
    v = v_.norm()
    assert is_perp_to_basis_vectors(v)

    cross_prod = BasisVectors.e2.cross(v)

    return cross_prod


def determine_normal_direction(v: geom.Vector):
    normal_vector = compute_outward_normal_assuming_cw(v)
    return CardinalDirections().get_drn_by_vector(normal_vector)
