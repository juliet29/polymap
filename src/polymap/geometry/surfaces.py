from dataclasses import dataclass

import geom
from utils4plans.geom import Coord
from utils4plans.lists import sort_and_group_objects

from polymap.geometry.vectors import (
    Direction,
    determine_normal_direction,
    Axes,
    get_normal_vector_assuming_cw,
)
from polymap.geometry.paired_coords import PairedCoord
from polymap.geometry.range import FancyRange


SMALL_SURFACE_SIZE = 0.15


def coords_to_range(coords: PairedCoord, ax: Axes):
    if ax == "X":
        return FancyRange(*sorted([i.x for i in coords]))
    else:
        return FancyRange(*sorted([i.y for i in coords]))


def coords_to_location(coords: PairedCoord, ax: Axes):
    if ax == "X":
        return coords[0].y
    else:
        return coords[0].x


@dataclass
class Surface:
    direction: Direction
    coords: PairedCoord
    vector: geom.Vector
    domain_name: str
    direction_ix: int = -1

    def __rich_repr__(self):
        yield "domain_name", self.domain_name
        yield "direction", self.direction.name
        yield "ix", self.direction_ix
        yield "range", repr(self.range)
        yield "size", f"{self.range.size:.4f}"
        yield "location", f"{self.location:.4f}"
        # yield "vector", self.vector
        yield "vector_norm", self.vector.norm()

    def __str__(self) -> str:
        return f"{self.domain_name}-{self.direction.name}_{self.direction_ix}"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Surface):
            return (
                (self.direction == other.direction)
                and (self.coords == other.coords)
                and (self.domain_name == other.domain_name)
                and (self.direction_ix == other.direction_ix)
            )
        raise Exception(f"Invalid object of type {type(other)}")

    def __hash__(self) -> int:
        return hash(self.direction.name) + hash(self.coords) + hash(self.domain_name)

    @property
    def name_w_domain(self):
        return str(self)

    @property
    def name(self):
        return f"{self.direction.name}_{self.direction_ix}"

    @property
    def short_name(self):
        return f"{self.direction.name[0].upper()}{self.direction_ix}"

    @property
    def parallel_axis(self):
        # NOTE: this is the axis that describes how the surface is oriented
        return self.direction.normal_axis

    @property
    def perpendicular_axis(self):
        return self.direction.aligned_axis

    @property
    def positive_perpendicular_vector(self):
        return self.direction.positive_vector

    @property
    def rounded_norm_vector(self):
        v = self.vector.norm()
        return geom.Vector(
            [round(i) for i in [v.x, v.y, v.z]]  # pyright: ignore[reportArgumentType]
        )  # normal vector is always positive!

    @property
    def aligned_vector(self):
        return get_normal_vector_assuming_cw(self.direction.name)

    @property
    def direction_vector(self):
        return self.direction.aligned_vector
        # v = self.vector.norm()
        # return geom.Vector(
        #     [round(i) for i in [v.x, v.y, v.z]]  # pyright: ignore[reportArgumentType]
        # ) # normal vector is always positive!

    # @property
    # def perpendicular_axis(self):
    #     # NOTE: this is the axis along which the surface can move
    #     return self.direction.aligned_axis

    @property
    def range(self):
        return coords_to_range(self.coords, self.parallel_axis)

    @property
    def location(self) -> float:
        return coords_to_location(self.coords, self.parallel_axis)

    @property
    def centroid(self):
        # TODO there is an easier way to do this with coords?
        if self.parallel_axis == "X":
            return Coord(self.range.midpoint, self.location)
        return Coord(
            self.location,
            self.range.midpoint,
        )

    @property
    def is_small(self):
        return self.range.size <= SMALL_SURFACE_SIZE

    def update_ix(self, ix: int):
        self.direction_ix = ix


def index_surfaces(surfaces: list[Surface]):
    grouped_surfaces = sort_and_group_objects(surfaces, lambda x: x.direction)

    def update_surfaces(surfs: list[Surface]):
        sorted_surfaces = sorted(surfs, key=lambda s: s.range.min)
        for ix, surf in enumerate(sorted_surfaces):
            surf.update_ix(ix)

    for group in grouped_surfaces:
        update_surfaces(group)

    return surfaces


def create_surface(v: geom.Vector, coords: PairedCoord, domain_name: str):
    direction = determine_normal_direction(v)
    assert direction, f"{geom.Vector} did not produce a matching direction"
    return Surface(direction, coords, v, domain_name)


def print_surfaces(surfs: list[Surface]):
    return [str(i) for i in surfs]
