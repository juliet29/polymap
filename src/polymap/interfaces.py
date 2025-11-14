from utils4plans.geom import Coord


from typing import NamedTuple


CoordsType = list[tuple[float | int, float | int]]


class PairedCoord(NamedTuple):
    first: Coord
    last: Coord

    def __str__(self):
        return f"PC[{self.first}, {self.last}]"

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

    # @property
    # def shapely_line(self):
    #     return sp.LineString([self.a.as_tuple, self.b.as_tuple])
