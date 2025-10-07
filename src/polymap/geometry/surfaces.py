from dataclasses import dataclass

import geom
from utils4plans.geom import Coord, Range
from utils4plans.lists import sort_and_group_objects

from polymap.geometry.vectors import Direction, determine_normal_direction, Axes
from polymap.interfaces import PairedCoord


@dataclass(frozen=True)
class FancyRange(Range):
    ...
    # TODO comparisons..


def coords_to_range(coords: PairedCoord, ax: Axes):
    if ax == "X":
        return FancyRange(*[i.x for i in coords])
    else:
        return FancyRange(*[i.y for i in coords])


def coords_to_location(coords: PairedCoord, ax: Axes):
    if ax == "X":
        return coords[0].y
    else:
        return coords[0].x


@dataclass
class Surface:
    direction: Direction
    coords: PairedCoord
    domain_name: str
    direction_ix: int = -1

    @property
    def range(self):
        return coords_to_range(self.coords, self.direction.normal_axis)

    @property
    def location(self) -> float:
        return coords_to_location(self.coords, self.direction.normal_axis)

    def update_ix(self, ix: int):
        self.direction_ix = ix


def index_surfaces(surfaces: list[Surface]):
    # # TODO split by direction
    # # check that there is only one direction..
    # drns = [i.direction for i in surfaces]
    # assert len(set(drns)) == 1

    grouped_surfaces = sort_and_group_objects(surfaces, lambda x: x.direction)

    def update_surfaces(surfs: list[Surface]):
        sorted_surfaces = sorted(surfs, key=lambda s: s.location)
        for ix, surf in enumerate(sorted_surfaces):
            surf.update_ix(ix)

    for group in grouped_surfaces:
        update_surfaces(group)

    return surfaces


def vector_to_surface(v: geom.Vector, coords: PairedCoord, domain_name: str):
    direction = determine_normal_direction(v)
    assert direction, f"{geom.Vector} did not produce a matching direction"
    return Surface(direction, coords, domain_name)
