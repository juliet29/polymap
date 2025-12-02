from polymap.nonortho.interfaces import RotatedLinearGeoms
from polymap.geometry.vectors import BasisVectors2D as bv
import pytest
import geom
from polymap.nonortho.dot import get_aligned_vector

ro = RotatedLinearGeoms.gen()

vpairs: list[tuple[geom.Vector, geom.Vector, geom.Vector]] = [
    (ro.e0.a10, bv.e0, bv.e1),
    (ro.e0.n_a10, bv.e0, bv.e1),
    (ro.n_e0.a10, -bv.e0, bv.e1),
    (ro.n_e0.a10, -bv.e0, bv.e1),
    (ro.e1.a10, bv.e1, bv.e0),
    (ro.e1.n_a10, bv.e1, bv.e0),
    (ro.n_e1.a10, -bv.e1, bv.e0),
    (ro.n_e1.a10, -bv.e1, bv.e0),
]


@pytest.mark.parametrize("v, basis, opp_basis", vpairs)
def test_align_vectors(v: geom.Vector, basis: geom.Vector, opp_basis: geom.Vector):
    res = get_aligned_vector(v)
    assert res.dot(basis) > 0  # correct pos or neg direction
    assert res.dot(opp_basis) == 0  # orthogonolized correctly
