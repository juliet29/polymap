from copy import deepcopy
import matplotlib.pyplot as plt
import shapely as sp
from typing import NamedTuple
from utils4plans.geom import Coord, tuple_list_from_list_of_coords
from polymap.geometry.ortho import FancyOrthoDomain
from polymap.geometry.surfaces import Surface
from polymap.geometry.vectors import (
    is_perpendicular,
    make_vector_2D,
    vector2D_from_coord,
    vector_as_coord,
    vector_from_coords,
)
from polymap.interfaces import PairedCoord, coords_from_paired_coords_list
import geom

from polymap.visuals.visuals import plot_polygon


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
    for item in update_coords_tuple:
        paired_coords[item.ix] = item.paired_coord

    return paired_coords


# TODO: put this shapely validation stuff in a different file
class InvalidPolygonError(Exception):
    def __init__(
        self, p: sp.Polygon, domain_name: str, reason: str, debug: bool = True
    ) -> None:
        self.p = p
        self.domain_name = domain_name
        self.reason = reason

        self.message()

        if debug:
            self.plot()

    def message(self):
        return f"{self.domain_name} is invalid! Reason: {self.reason}"

    def plot(self):
        fig, ax = plt.subplots()
        plot_polygon(self.p, ax=ax)
        ax.set_title(f"Failing polygon: {self.domain_name}")
        plt.show()


def validate_polygon(p: sp.Polygon, domain_name: str, debug=False):
    if len(p.interiors) != 0:
        raise InvalidPolygonError(p, domain_name, "Num interiors != 0")
    if not p.is_valid:
        reason = sp.is_valid_reason(p)
        raise InvalidPolygonError(p, domain_name, reason, debug)


def update_domain(
    domain: FancyOrthoDomain, surface: Surface, location_delta: float, debug=False
):
    # NOTE: not sure this is correct, but lets just try the aligned vecto and see what happens
    vector = make_vector_2D(surface.direction.aligned_vector) * location_delta
    # NOTE: the aligned vector already has a direction! would be nice if can fix so that south rooms can only move south.. but think the graph will determine this ..

    updated_paired_coords = update_paired_coords(
        domain.paired_coords, surface.coords, vector
    )

    coords = coords_from_paired_coords_list(updated_paired_coords)

    test_poly = sp.Polygon(tuple_list_from_list_of_coords(coords))
    validate_polygon(test_poly, domain.name, debug)

    return FancyOrthoDomain(coords=coords, name=domain.name)
