import geom
from polymap.nonortho.interfaces import RotatedLinearGeoms
from polymap.geometry.vectors import BasisVectors2D, BaseVectorNames
from rich import print
from typing import NamedTuple


class DotProdCombo(NamedTuple):
    basis: geom.Vector
    dot_prod: float


def get_aligned_vector(v: geom.Vector):
    dot_prods = [DotProdCombo(b, v.dot(b)) for b in BasisVectors2D.vectors]
    sorted_dot_prods = sorted(dot_prods, key=lambda x: x.dot_prod, reverse=True)
    print(sorted_dot_prods)
    res = sorted_dot_prods[0]
    fres = res.basis * res.dot_prod
    print(fres)
    # TODO throw error for large angles 
    return fres


if __name__ == "__main__":
    ro = RotatedLinearGeoms.gen()
    get_aligned_vector(ro.n_e0.a10)
