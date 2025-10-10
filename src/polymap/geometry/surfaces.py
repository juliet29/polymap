from dataclasses import dataclass

import geom
import shapely as sp
from utils4plans.geom import Coord, Range
from utils4plans.lists import sort_and_group_objects

from polymap.geometry.vectors import Direction, determine_normal_direction, Axes
from polymap.interfaces import PairedCoord

import numpy as np


@dataclass(frozen=True)
class FancyRange(Range):
    def __lt__(self, other):
        if isinstance(other, FancyRange):
            return self.size < other.size
        raise Exception(
            f"Invalid comparison for object of type {type(other)}"
        )  # TODO include picture for this?

    @property
    def as_np_range(self):
        return np.arange(self.min, self.max, 0.01)

    @property
    def as_tuple(self):
        return (self.min, self.max)

    @property
    def size(self):
        return self.max - self.min

    @property
    def midpoint(self):
        return (self.min + self.max) / 2

    def is_coincident(self, other):
        if isinstance(other, FancyRange):
            if other.max <= self.min or other.min >= self.max:
                return False
            return True
        raise Exception(
            f"Invalid comparison for object of type {type(other)}"
        )  # TODO include picture for this?

    def contains(self, other):
        if isinstance(other, FancyRange):
            if (other.min >= self.min) and (other.max <= self.max):
                return True
            return False
        raise Exception(f"Invalid comparison for object of type {type(other)}")


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


def coords_from_range_and_location(range: FancyRange, location: float, ax: Axes):
    if ax == "X":
        c1 = (range.min, location)
        c2 = (range.max, location)
    else:
        c1 = (
            location,
            range.min,
        )
        c2 = (
            location,
            range.max,
        )
    return PairedCoord(Coord(*c1), Coord(*c2))


@dataclass
class Surface:
    direction: Direction
    coords: PairedCoord
    domain_name: str
    direction_ix: int = -1

    def __rich_repr__(self):
        yield "domain_name", self.domain_name
        yield "direction", self.direction.name
        yield "ix", self.direction_ix
        yield "range", self.range
        yield "location", self.location

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
    def aligned_axis(self):
        return self.direction.normal_axis

    @property
    def direction_axis(self):
        return self.direction.aligned_axis

    @property
    def range(self):
        return coords_to_range(self.coords, self.aligned_axis)

    @property
    def location(self) -> float:
        return coords_to_location(self.coords, self.aligned_axis)

    @property
    def centroid(self):
        # TODO there is an easier way to do this with coords?
        if self.aligned_axis == "X":
            return Coord(self.range.midpoint, self.location)
        return Coord(
            self.location,
            self.range.midpoint,
        )

    def update_ix(self, ix: int):
        self.direction_ix = ix

    def update_surface_location(self, num: float):
        new_loc = self.location + num
        new_coords = coords_from_range_and_location(
            self.range, new_loc, self.aligned_axis
        )
        return Surface(self.direction, new_coords, self.domain_name, self.direction_ix)

    # def is_crossing(self, shape: sp.Polygon):
    #     line = self.coords.shapely_line
    #     return line.crosses(shape)


def index_surfaces(surfaces: list[Surface]):
    grouped_surfaces = sort_and_group_objects(surfaces, lambda x: x.direction)

    def update_surfaces(surfs: list[Surface]):
        sorted_surfaces = sorted(surfs, key=lambda s: s.location)
        for ix, surf in enumerate(sorted_surfaces):
            surf.update_ix(ix)

    for group in grouped_surfaces:
        update_surfaces(group)

    return surfaces


def create_surface(v: geom.Vector, coords: PairedCoord, domain_name: str):
    direction = determine_normal_direction(v)
    assert direction, f"{geom.Vector} did not produce a matching direction"
    return Surface(direction, coords, domain_name)
