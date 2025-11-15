from copy import deepcopy
from typing import NamedTuple
from utils4plans.geom import Coord
from polymap.geometry.vectors import (
    is_perpendicular,
    vector2D_from_coord,
    vector_as_coord,
    vector_from_coords,
)
from polymap.interfaces import PairedCoord
import geom


# class PairedCoordList:
#     values: list[PairedCoord]
#
#     def get_coord_ix(self, pc: PairedCoord):
#         pass


class UpdateCoordsInfo(NamedTuple):
    paired_coord: PairedCoord
    ix: int

    def __repr__(self):
        return f"{self.ix}: {str(self.paired_coord)}"


class UpdateCoordsTuple(NamedTuple):
    alpha: UpdateCoordsInfo
    target: UpdateCoordsInfo
    beta: UpdateCoordsInfo

    def __repr__(self):
        return f"{self._asdict()}"


def apply_vector_to_paired_coord(pc: PairedCoord, vector: geom.Vector):
    def apply(coord: Coord):
        res = vector2D_from_coord(coord) + vector
        return vector_as_coord(res)

    return PairedCoord(*[apply(i) for i in pc])


def is_vector_orthogonal(target: PairedCoord, vector: geom.Vector):
    target_v = vector_from_coords(*target, _2D=True)
    return is_perpendicular(target_v, vector)


def create_update_coords_tuple(
    paired_coords_: list[PairedCoord], target: PairedCoord, vector: geom.Vector
):
    assert is_vector_orthogonal(target, vector)
    paired_coords = deepcopy(paired_coords_)
    target_ix = paired_coords.index(target)

    alpha_ix = (target_ix - 1) % len(paired_coords)

    beta_ix = (target_ix + 1) % len(paired_coords)

    alpha, beta = paired_coords[alpha_ix], paired_coords[beta_ix]

    new_target = apply_vector_to_paired_coord(target, vector)
    target_info = UpdateCoordsInfo(new_target, target_ix)
    alpha_info = UpdateCoordsInfo(PairedCoord(alpha.first, new_target.first), alpha_ix)
    beta_info = UpdateCoordsInfo(PairedCoord(new_target.last, beta.last), beta_ix)

    return UpdateCoordsTuple(alpha_info, target_info, beta_info)


def update_domain():
    pass
