from copy import deepcopy
from utils4plans.geom import Coord
from polymap.geometry.vectors import vector2D_from_coord, vector_as_coord
from polymap.interfaces import PairedCoord
import geom


class PairedCoordList:
    values: list[PairedCoord]

    def get_coord_ix(self, pc: PairedCoord):
        pass


def apply_vector_to_paired_coord(pc: PairedCoord, vector: geom.Vector):
    def apply(coord: Coord):
        res = vector2D_from_coord(coord) + vector
        return vector_as_coord(res)

    return PairedCoord(*[apply(i) for i in pc])


def update_paired_coords(
    paired_coords_: list[PairedCoord], target: PairedCoord, vector: geom.Vector
):
    paired_coords = deepcopy(paired_coords_)
    target_ix = paired_coords.index(target)
    alpha_ix, beta_ix = target_ix - 1, target_ix + 1
    alpha, beta = paired_coords[alpha_ix], paired_coords[beta_ix]
    # TODO: what if this the first or last item?? -> can use cycle or can do manually.., see if there is a python fx in itertools that is soley for wrap around indexing..

    new_target = apply_vector_to_paired_coord(target, vector)
    paired_coords[target_ix] = new_target
    paired_coords[alpha_ix] = PairedCoord(alpha.first, new_target.first)
    paired_coords[beta_ix] = PairedCoord(new_target.last, beta.last)

    return paired_coords


def update_domain():
    pass
