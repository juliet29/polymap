from polymap.examples.sample_domains import create_ortho_domain
from rich import print
import geom
import pytest
from utils4plans.geom import Coord


def test_create_shapely():
    domain = create_ortho_domain()
    p = domain.shapely_polygon
    assert p.is_valid


def test_normalize_coords_are_cw():
    domain = create_ortho_domain("SQUARE")
    coords = domain.normalized_coords
    expected_coords = [
        (0, 0),
        (0, 1),
        (1, 1),
        (1, 0),
        (0, 0),
    ]
    assert coords == [Coord(*i) for i in expected_coords]


def test_vectors_bottom_up_l():
    domain = create_ortho_domain()
    expected_vectors = [  # TODO put this somewhere safe!
        geom.Vector([0.0, 2.0, 0]),
        geom.Vector([2.0, 0.0, 0]),
        geom.Vector([0.0, -1.0, 0]),
        geom.Vector([-1.0, 0.0, 0]),
        geom.Vector([0.0, -1.0, 0]),
        geom.Vector([-1.0, 0.0, 0]),
    ]
    assert domain.vectors == expected_vectors


def test_orthogonal():
    domain = create_ortho_domain()
    assert domain.is_orthogonal


def test_is_not_orthogonal():
    domain = create_ortho_domain("NON_ORTHO")
    with pytest.raises(AssertionError):
        assert domain.is_orthogonal


if __name__ == "__main__":
    domain = create_ortho_domain()
    print(domain.vectors)
    print(domain.is_orthogonal)
