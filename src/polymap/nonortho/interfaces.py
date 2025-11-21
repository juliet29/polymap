from typing import NamedTuple
import shapely as sp
from polymap.geometry.vectors import sp_line_to_vector
import geom

ORIGIN = (0, 0)

# TODO turn to class
X1 = (1, 0)
Y1 = (0, 1)
nX1 = (-1, 0)
nY1 = (0, -1)
e0 = sp.LineString([ORIGIN, X1])
e1 = sp.LineString([ORIGIN, Y1])
n_e0 = sp.LineString([ORIGIN, nX1])
n_e1 = sp.LineString([ORIGIN, nY1])
base_line_strings = [e0, e1, n_e0, n_e1]


# class LineVector(NamedTuple):
#     line: sp.LineString
#     v: geom.Vector


class LinearGeoms(NamedTuple):
    a10: geom.Vector
    a15: geom.Vector
    a20: geom.Vector
    a45: geom.Vector
    n_a10: geom.Vector
    n_a15: geom.Vector
    n_a20: geom.Vector
    n_a45: geom.Vector


# class BaseGeoms(NamedTuple):
#     e0: LineVector
#     e1: LineVector
#     n_e0: LineVector
#     n_e1: LineVector


class RotatedLinearGeoms(NamedTuple):
    e0: LinearGeoms
    e1: LinearGeoms
    n_e0: LinearGeoms
    n_e1: LinearGeoms

    @classmethod
    def gen(cls):
        def create_data_for_base_vector(e: sp.LineString):
            e_lines = [sp.affinity.rotate(e, angle, origin=ORIGIN) for angle in angles]
            return LinearGeoms(*[sp_line_to_vector(i) for i in e_lines])

        angles_base = [10, 15, 20, 45]
        angles = angles_base + [-1 * i for i in angles_base]

        return cls(*[create_data_for_base_vector(i) for i in base_line_strings])


# def create_base_lines():
#     vectors = [sp_line_to_vector(i) for i in base_line_strings]
#     return BaseGeoms(*[LineVector(i, j) for i, j in zip(base_line_strings, vectors)])


# def plot_lines(lg: LinearGeoms):
#     plot_line(sp.MultiLineString([i.line for i in lg]))
