from copy import deepcopy

from polymap.interfaces import CoordsType


square: CoordsType = [(0, 0), (0, 1), (1, 1), (1, 0)]
ldom: CoordsType = [(0, 0), (0, 1), (0.5, 1), (0.5, 0.3), (1, 0.3), (1, 0)]
crook = (0.5, 0.3)


class KappaExamples:
    @property
    def one(self):
        nc = [(0.5, 1), (0.5, 0.9)]
        coords = deepcopy(square)
        coords[2] = (1, 0.9)
        start_ix = 2

        for ix, coord in enumerate(nc):
            coords.insert(start_ix + ix, coord)

        return coords

    @property
    def two_out(self):
        nc = [(0.5, 0.4), (0.6, 0.4), (0.6, 0.3)]
        coords = deepcopy(ldom)
        start_ix = coords.index(crook)
        for ix, coord in enumerate(nc):
            coords.insert(start_ix + ix, coord)
        coords.remove(crook)
        return coords

    @property
    def two_in(self):
        nc = [(0.5, 0.4), (0.4, 0.4), (0.4, 0.3)]
        coords = deepcopy(ldom)
        start_ix = coords.index(crook)
        for ix, coord in enumerate(nc):
            coords.insert(start_ix + ix, coord)
        coords.remove(crook)
        return coords


class PiExamples:

    def make_coords(self, dx: float, dy: float):
        xl = 0.4
        yt = 1
        xr = xl + dx
        yb = yt - dy
        nc = [(xl, yt), (xl, yb), (xr, yb), (xr, yt)]
        coords = deepcopy(square)
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


class BendExamples:
    kappa = KappaExamples()
    pi = PiExamples()
