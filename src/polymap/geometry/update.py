from copy import deepcopy
from typing import NamedTuple
from utils4plans.geom import Coord
from polymap.geometry.vectors import vector2D_from_coord, vector_as_coord
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

    # def __eq__(self, other: object) -> bool:
    #     if isinstance(other, UpdateCoordsInfo):
    #         return (self.ix == other.ix) and (self.paired_coord == other.paired_coord)
    #     raise ValueError("Invalid comparison")


class UpdateCoordsTuple(NamedTuple):
    alpha: UpdateCoordsInfo
    target: UpdateCoordsInfo
    beta: UpdateCoordsInfo
    #
    # def __eq__(self, other: object) -> bool:
    #     if isinstance(other, UpdateCoordsTuple):
    #         return
    #     raise ValueError("Invalid comparison")

    # def __repr__(self):
    #     return


def apply_vector_to_paired_coord(pc: PairedCoord, vector: geom.Vector):
    def apply(coord: Coord):
        res = vector2D_from_coord(coord) + vector
        return vector_as_coord(res)

    return PairedCoord(*[apply(i) for i in pc])


def create_update_coords_tuple(
    paired_coords_: list[PairedCoord], target: PairedCoord, vector: geom.Vector
):
    paired_coords = deepcopy(paired_coords_)
    target_ix = paired_coords.index(target)
    alpha_ix, beta_ix = target_ix - 1, target_ix + 1

    alpha, beta = paired_coords[alpha_ix], paired_coords[beta_ix]
    # TODO: what if this the first or last item?? -> can use cycle or can do manually.., see if there is a python fx in itertools that is soley for wrap around indexing..

    new_target = apply_vector_to_paired_coord(target, vector)
    target_info = UpdateCoordsInfo(new_target, target_ix)
    alpha_info = UpdateCoordsInfo(PairedCoord(alpha.first, new_target.first), alpha_ix)
    beta_info = UpdateCoordsInfo(PairedCoord(new_target.last, beta.last), beta_ix)

    return UpdateCoordsTuple(alpha_info, target_info, beta_info)


def update_domain():
    pass
