from typing import NamedTuple, Literal
from rich import print
import shapely as sp
from polymap.geometry.vectors import sp_line_to_vector
from polymap.visuals import plot_line
import geom

ORIGIN = (0, 0)
X1 = (1, 0)
Y1 = (0, 1)
nX1 = (-1, 0)
nY1 = (0, -1)
e0 = sp.LineString([ORIGIN, X1])
e1 = sp.LineString([ORIGIN, Y1])
n_e0 = sp.LineString([ORIGIN, nX1])
n_e1 = sp.LineString([ORIGIN, nY1])
base_line_strings = [e0, e1, n_e0, n_e1]


class LineVector(NamedTuple):
    line: sp.LineString
    v: geom.Vector


class LinearGeoms(NamedTuple):
    a10: LineVector
    a15: LineVector
    a20: LineVector
    a45: LineVector
    n_a10: LineVector
    n_a15: LineVector
    n_a20: LineVector
    n_a45: LineVector


class BaseGeoms(NamedTuple):
    e0: LineVector
    e1: LineVector
    n_e0: LineVector
    n_e1: LineVector


class RotatedLinearGeoms(NamedTuple):
    e0: LinearGeoms
    e1: LinearGeoms
    n_e0: LinearGeoms
    n_e1: LinearGeoms


def create_base_lines():
    vectors = [sp_line_to_vector(i) for i in base_line_strings]
    return BaseGeoms(*[LineVector(i, j) for i, j in zip(base_line_strings, vectors)])


def create_test_lines():
    def create_data_for_base_vector(e: sp.LineString):
        e_lines = [sp.affinity.rotate(e, angle, origin=ORIGIN) for angle in angles]
        e_vectors = [sp_line_to_vector(i) for i in e_lines]
        return LinearGeoms(*[LineVector(i, j) for i, j in zip(e_lines, e_vectors)])

    angles_base = [10, 15, 20, 45]
    angles = angles_base + [-1 * i for i in angles_base]

    return RotatedLinearGeoms(
        *[create_data_for_base_vector(i) for i in base_line_strings]
    )


def plot_lines(lg: LinearGeoms):
    plot_line(sp.MultiLineString([i.line for i in lg]))
