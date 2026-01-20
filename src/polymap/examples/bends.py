from copy import deepcopy

from polymap.geometry.ortho import FancyOrthoDomain
from utils4plans.geom import CoordsType


class Geom:
    square: CoordsType = [(0, 0), (0, 1), (1, 1), (1, 0)]
    ldom: CoordsType = [(0, 0), (0, 1), (0.5, 1), (0.5, 0.3), (1, 0.3), (1, 0)]
    crook = (0.5, 0.3)


class KappaExamples:
    g = Geom()

    @property
    def one(self):
        nc = [(0.5, 1), (0.5, 0.9)]
        coords = deepcopy(self.g.square)
        coords[2] = (1, 0.9)
        start_ix = 2

        for ix, coord in enumerate(nc):
            coords.insert(start_ix + ix, coord)

        return coords

    @property
    def two_out(self):
        nc = [(0.5, 0.4), (0.6, 0.4), (0.6, 0.3)]
        coords = deepcopy(self.g.ldom)
        start_ix = coords.index(self.g.crook)
        for ix, coord in enumerate(nc):
            coords.insert(start_ix + ix, coord)
        coords.remove(self.g.crook)
        return coords

    @property
    def two_in(self):
        nc = [(0.5, 0.4), (0.4, 0.4), (0.4, 0.3)]
        coords = deepcopy(self.g.ldom)
        start_ix = coords.index(self.g.crook)
        for ix, coord in enumerate(nc):
            coords.insert(start_ix + ix, coord)
        coords.remove(self.g.crook)
        return coords

    @property
    def all(self):
        return [self.one, self.two_out, self.two_in]

    @property
    def names(self):
        return [f"kappa{n}" for n in [1, "2out", "2in"]]


class PiExamples:
    g = Geom()

    def make_coords(self, dx: float, dy: float):
        xl = 0.4
        yt = 1
        xr = xl + dx
        yb = yt - dy
        nc = [(xl, yt), (xl, yb), (xr, yb), (xr, yt)]
        coords = deepcopy(self.g.square)
        start_ix = 2

        for ix, coord in enumerate(nc):
            coords.insert(start_ix + ix, coord)

        return coords

    @property
    def one(self):
        return self.make_coords(dx=0.1, dy=0.5)

    @property
    def two(self):
        return self.make_coords(dx=0.5, dy=0.1)

    @property
    def three(self):
        return self.make_coords(dx=0.1, dy=0.1)

    @property
    def all(self):
        return [self.one, self.two, self.three]

    @property
    def names(self):
        return [f"pi{i+1}" for i in range(3)]


class BendExamples:
    kappa = KappaExamples()
    pi = PiExamples()

    @property
    def all(self):
        return self.kappa.all + self.pi.all

    @property
    def names(self):
        return self.kappa.names + self.pi.names

    @property
    def all_doms(self):
        return [
            FancyOrthoDomain.from_tuple_list(i, j) for i, j in zip(self.all, self.names)
        ]
