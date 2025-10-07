from utils4plans.geom import Coord


from typing import NamedTuple


CoordsType = list[tuple[float | int, float | int]]


class PairedCoord(NamedTuple):
    a: Coord
    b: Coord
