from dataclasses import dataclass
import shapely as sp

from utils4plans.geom import Coord, Range

from polymap.geometry.vectors import Axes
from polymap.geometry.paired_coords import PairedCoord

import numpy as np


def coords_from_range_and_location(range: Range, location: float, ax: Axes):
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


def coords_to_normal_range(coords: PairedCoord, ax: Axes):
    if ax == "X":
        return Range(*sorted([i.x for i in coords]))
    else:
        return Range(*sorted([i.y for i in coords]))


def compute_intersection(r1: Range, r2: Range, ax: Axes):
    l1 = coords_from_range_and_location(r1, 0, ax).shapely_line
    l2 = coords_from_range_and_location(r2, 0, ax).shapely_line
    inter = l1.intersection(l2)
    assert isinstance(inter, sp.LineString)
    inter_coords = PairedCoord(*[Coord(*i) for i in inter.coords])
    return coords_to_normal_range(inter_coords, ax)


@dataclass(frozen=True)
class FancyRange(Range):
    def __repr__(self) -> str:
        return super().__repr__()

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

    def intersection(self, other, ax: Axes):
        if isinstance(other, FancyRange):
            inter_range = compute_intersection(self, other, ax)
            return FancyRange(inter_range.min, inter_range.max)

        raise Exception(f"Invalid comparison for object of type {type(other)}")
