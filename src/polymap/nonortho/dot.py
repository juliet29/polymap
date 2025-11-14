import geom
from polymap.nonortho.interfaces import RotatedLinearGeoms
from polymap.geometry.vectors import BasisVectors2D, BaseVectorNames
from rich import print
from typing import NamedTuple
from utils4plans.geom import Coord


class DotProdCombo(NamedTuple):
    basis: geom.Vector
    dot_prod: float


def add_coord_and_vector(c: Coord, v: geom.Vector):
    vx, vy = float(v[0]), float(v[1])  # type: ignore
    return Coord(vx + c.x, vy + c.y)


def get_aligned_vector(v: geom.Vector):
    dot_prods = [DotProdCombo(b, v.dot(b)) for b in BasisVectors2D.vectors]
    sorted_dot_prods = sorted(dot_prods, key=lambda x: x.dot_prod, reverse=True)
    # print(sorted_dot_prods)
    res = sorted_dot_prods[0]
    fres = res.basis * res.dot_prod
    print(f"vector to align: {v} | result: {fres}")
    # TODO throw error for large angles
    return fres


def make_ortho_coords(coords: list[Coord], vectors: list[geom.Vector]):
    aligned_vectors = [get_aligned_vector(i) for i in vectors]
    new_coords: list[Coord] = [] # = [coords[0]]

    for coord, v in zip(coords[0:-1], aligned_vectors):
        new_coord = add_coord_and_vector(coord, v)
        new_coords.append(new_coord)
    # new_coords.append(coords[0])

    return new_coords


if __name__ == "__main__":
    ro = RotatedLinearGeoms.gen()
    get_aligned_vector(ro.n_e0.a10)
