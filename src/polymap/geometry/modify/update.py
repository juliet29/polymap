from copy import deepcopy
import shapely as sp
from typing import NamedTuple
from utils4plans.geom import Coord, tuple_list_from_list_of_coords
from utils4plans.lists import get_unique_items_in_list_keep_order
from polymap.geometry.ortho import FancyOrthoDomain
from polymap.geometry.shapely_helpers import get_coords_from_shapely_polygon
from polymap.geometry.surfaces import Surface
from polymap.geometry.vectors import (
    is_perpendicular,
    make_vector_2D,
    vector2D_from_coord,
    vector_as_coord,
    vector_from_coords,
)
from polymap.geometry.paired_coords import (
    PairedCoord,
    coords_from_paired_coords_list,
)
import geom
from polymap.geometry.modify.validate import InvalidPolygonError, validate_polygon


class Move(NamedTuple):
    domain: FancyOrthoDomain
    surface: Surface
    delta: float

    def __str__(self) -> str:
        return f"[green italic]Moving {self.surface.name_w_domain} by {self.delta:.4f}"

    def summary(self) -> str:
        return f"[green italic]Moving {self.surface.name_w_domain} by {self.delta}"


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
    paired_coords: list[PairedCoord], target: PairedCoord, vector: geom.Vector
):
    assert is_vector_orthogonal(target, vector)

    target_ix = paired_coords.index(target)
    alpha_ix = (target_ix - 1) % len(paired_coords)
    beta_ix = (target_ix + 1) % len(paired_coords)
    alpha, beta = paired_coords[alpha_ix], paired_coords[beta_ix]

    new_target = apply_vector_to_paired_coord(target, vector)

    target_info = UpdateCoordsInfo(new_target, target_ix)
    alpha_info = UpdateCoordsInfo(PairedCoord(alpha.first, new_target.first), alpha_ix)
    beta_info = UpdateCoordsInfo(PairedCoord(new_target.last, beta.last), beta_ix)

    return UpdateCoordsTuple(alpha_info, target_info, beta_info)


def update_paired_coords(
    paired_coords_: list[PairedCoord], target: PairedCoord, vector: geom.Vector
):
    paired_coords = deepcopy(paired_coords_)
    update_coords_tuple = create_update_coords_tuple(paired_coords, target, vector)
    # print(update_coords_tuple)
    for item in update_coords_tuple:
        paired_coords[item.ix] = item.paired_coord

    return paired_coords


def remove_zero_vector_coords(pcs: list[PairedCoord]):

    vectors = list(map(lambda x: vector_from_coords(*x), pcs))

    new_pcs = []
    for v, pc in zip(vectors, pcs):
        if v.mag() != 0:
            new_pcs.append(pc)

    return new_pcs


def update_domain(move: Move):
    domain, surface, location_delta = move
    # logger.debug(str(move))
    vector = (
        make_vector_2D(surface.positive_perpendicular_vector) * location_delta
    )  # TODO: this is likely the source of instability...
    # d = {
    #     "vx": get_component(vector, "x"),
    #     "vy": get_component(vector, "y"),
    #     "true": location_delta,
    # }
    # logger.trace(f"{d}")
    # is_eq = d["vx"] == location_delta
    # logger.trace(f"{is_eq=}")

    updated_paired_coords = update_paired_coords(
        domain.paired_coords, surface.coords, vector
    )
    # print(updated_paired_coords)

    non_zero_paired_coords = remove_zero_vector_coords(updated_paired_coords)
    coords = coords_from_paired_coords_list(non_zero_paired_coords)
    new_coords = tuple_list_from_list_of_coords(coords)

    # NOTE: this is a change to accomadate bends, may mess with the larger matching algo 25/12/10
    unique_coords = get_unique_items_in_list_keep_order(new_coords)

    try:
        test_poly = sp.Polygon(unique_coords)
    except ValueError as e:
        raise InvalidPolygonError(
            sp.Polygon(),
            domain.name,
            f"Not enough coords to create polygon! {unique_coords}: {e}",
        )

    validate_polygon(test_poly, domain.name)

    new_dom = FancyOrthoDomain(
        coords=get_coords_from_shapely_polygon(test_poly), name=domain.name
    )

    # old_coords = move.domain.normalized_coords
    # new_coords = new_dom.normalized_coords
    # dif_coords = set_difference(old_coords, new_coords)
    #
    # logger.debug(len(dif_coords))
    #
    return new_dom
