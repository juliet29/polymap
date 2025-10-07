from polymap.examples.sample_domains import create_ortho_domain
from rich import print
import geom


def test_create_shapely():
    domain = create_ortho_domain()
    p = domain.shapely_polygon
    assert p.is_valid


def test_vectors():
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


if __name__ == "__main__":
    domain = create_ortho_domain()
    print(domain.vectors)
    print(domain.is_orthogonal)
