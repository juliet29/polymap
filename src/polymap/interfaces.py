from utils4plans.geom import Coord
import shapely as sp


from typing import NamedTuple


CoordsType = list[tuple[float | int, float | int]]


class PairedCoord(NamedTuple):
    a: Coord
    b: Coord

    @property
    def as_list(self):
        return [self.a, self.b]

    # @property
    # def shapely_line(self):
    #     return sp.LineString([self.a.as_tuple, self.b.as_tuple])
