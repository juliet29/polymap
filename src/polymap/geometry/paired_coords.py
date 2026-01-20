from itertools import cycle
from typing import NamedTuple
import shapely as sp

from utils4plans.geom import Coord
from utils4plans.lists import pairwise


class PairedCoord(NamedTuple):
    first: Coord
    last: Coord

    def __str__(self):
        return f"PairedCoord[{self.first}, {self.last}]"

    def __eq__(self, other: object, /) -> bool:
        if isinstance(other, PairedCoord):
            return self.first == other.first and self.last == other.last
        else:
            raise ValueError("Invalid comparison")

    def __lt__(self, other: object, /) -> bool:
        if isinstance(other, PairedCoord):
            return (other.first, other.last) < (self.first, self.last)
        else:
            raise ValueError("Invalid comparison")

    @property
    def as_list(self):
        return [self.first, self.last]

    @property
    def shapely_line(self):
        return sp.LineString([self.first.as_tuple, self.last.as_tuple])

    #
    #


def coords_from_paired_coords_list(pcs: list[PairedCoord]):
    return [i.last for i in pcs]


def print_paired_coords(pcs: list[PairedCoord]):
    for ix, pc in enumerate(pcs):
        print(f"{ix}: {str(pc)}")


def create_paired_coords(coords: list[Coord]):
    num_coords = len(coords)
    count = 0
    paired_coords: list[PairedCoord] = []
    for i, j in pairwise(cycle(coords)):
        paired_coords.append(PairedCoord(i, j))

        count += 1
        if count > num_coords - 2:
            break
    assert paired_coords[0].first == paired_coords[-1].last

    return paired_coords
