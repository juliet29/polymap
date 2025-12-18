from utils4plans.geom import Coord
import shapely as sp
from rich import print

from typing import NamedTuple, Any, Generator, Callable


GraphPairs = dict[str, list[str]]
CoordsType = list[tuple[float | int, float | int]]


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


def make_repr(fx: Callable[[], Generator[tuple[str, Any]]], obj: object | str):
    repr_str: list[str] = []
    append = repr_str.append
    inp = fx()
    for arg in inp:
        key, value = arg
        append(f"{key}={value}")
    if isinstance(obj, str):
        return f"{obj}({'\n '.join(repr_str)})"
    else:
        return f"{obj.__class__.__name__}({', '.join(repr_str)})"


def make_repr_obj(fx: Callable[[], Generator[tuple[str, Any]]]):
    inp = fx()
    d = {}
    for arg in inp:
        key, value = arg
        d[key] = value
    return d
    # if isinstance(obj, str):
    #     return f"{obj}({'\n '.join(repr_str)})"
    # else:
    #     return f"{obj.__class__.__name__}({', '.join(repr_str)})"
