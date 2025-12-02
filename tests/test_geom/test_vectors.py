import geom
import pytest
from utils4plans.geom import Coord
from polymap.geometry.vectors import (
    vector_from_coords,
    compute_outward_normal_assuming_cw,
    determine_normal_direction,
    CardinalDirections,
    Direction,
)

e0 = geom.Vector([1, 0, 0])
e1 = geom.Vector([0, 1, 0])
e2 = geom.Vector([0, 0, 1])
aligned = geom.Vector([3, 0, 0])


def test_magnitude():
    assert aligned.norm().mag() == 1


def test_dot_prod():
    assert e0.dot(aligned.norm()) == 1


vector_cross_group: list[tuple[geom.Vector, geom.Vector, geom.Vector]] = [
    (e0, e1, e2),  # ixj +
    (e1, e0, -e2),  # jxi -
    (e2, e0, e1),  # kxi +
    (e2, e1, -e0),  # kxj -
    (-e1, e2, -e0),
]


@pytest.mark.parametrize("v1, v2, result", vector_cross_group)
def test_cross_products(v1, v2, result):
    assert (v1.cross(v2)) == result


def test_create_vector_from_coords():
    c1 = Coord(1, 1)
    c2 = Coord(3, 3)

    res = vector_from_coords(c1, c2)
    expected_res = geom.Vector([2, 2, 0])
    assert res == expected_res


vector_normal_group: list[tuple[geom.Vector, geom.Vector]] = [
    (e0, e1),
    (-e1, e0),
    (-e0, -e1),
    (e1, -e0),
]


@pytest.mark.parametrize("v, result", vector_normal_group)
def test_compute_outward_normal_assuming_cw(v, result):
    assert compute_outward_normal_assuming_cw(v) == result


vector_drn_group: list[tuple[geom.Vector, Direction]] = [
    (e0, CardinalDirections.NORTH),
    (-e1, CardinalDirections.EAST),
    (-e0, CardinalDirections.SOUTH),
    (e1, CardinalDirections.WEST),
]


@pytest.mark.parametrize("v, result", vector_drn_group)
def test_compute_normal_direction(v, result):
    assert determine_normal_direction(v) == result


def test_positive_vector():
    drn = CardinalDirections.WEST
    assert drn.positive_vector == geom.Vector([1, 0, 0])
    assert drn.aligned_vector == geom.Vector([-1, 0, 0])


# def test_normal2():
#     e2 = geom.Vector([0, 0, 1])
#     new = geom.Vector([3, 2, 0])

#     print(e2.cross(new))


if __name__ == "__main__":
    compute_outward_normal_assuming_cw(e0)
