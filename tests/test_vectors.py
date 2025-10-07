import geom
from rich import print
import pytest
from utils4plans.geom import Coord
from polymap.geometry.vectors import vector_from_coords

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


# def test_normal2():
#     e2 = geom.Vector([0, 0, 1])
#     new = geom.Vector([3, 2, 0])

#     print(e2.cross(new))


if __name__ == "__main__":
    e2 = geom.Vector([0, 0, 1])
    new = geom.Vector([3, 2, 0])
    # manual_normal_calc(e2, new)
