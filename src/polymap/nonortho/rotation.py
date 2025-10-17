from polymap.geometry.vectors import vector_from_coords
from utils4plans.geom import Coord
import shapely as sp
from polymap.visuals import plot_line
from dataclasses import dataclass
import geom
import math
from typing import NamedTuple, Literal
from rich import print

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


def plot_lines(lg: LinearGeoms):
    plot_line(sp.MultiLineString([i.line for i in lg]))


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


def sp_line_to_vector(line: sp.LineString):
    coords = [Coord(*i) for i in line.coords]
    return vector_from_coords(*coords, _2D=False)


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


def calc_angle_between_vectors(v1: geom.Vector, v2: geom.Vector, deg=False):
    def clip_value(value, lower_bound=-1, upper_bound=1):
        return max(lower_bound, min(value, upper_bound))

    v1mag = abs(v1)
    v2mag = abs(v2)
    assert v1mag > 0 and v2mag > 0, (
        f"one of vectors has magnitude less than or equal to 0: {v1}, {v2}"
    )

    cos_theta = v1.dot(v2) / (v1mag * v2mag)
    assert cos_theta >= -1 and cos_theta <= 1, (
        f"cos_theta `{cos_theta}` should be -1 <= cos_theta <= 1"
    )

    theta = math.acos(clip_value(cos_theta))
    if deg:
        return math.degrees(theta)

    return theta  # TODO want to round this ideally..


BaseVectorNames = Literal["e0", "e1", "n_e0", "n_e1"]


class VectorAngle(NamedTuple):
    vector_name: BaseVectorNames
    angle: float


class AngleResult(NamedTuple):
    e0: float
    e1: float
    n_e0: float
    n_e1: float

    @property
    def smallest(self):
        d = self._asdict()
        base_vector, angle = sorted([(k, v) for k, v in d.items()], key=lambda x: x[1])[
            0
        ]
        return VectorAngle(base_vector, angle)  # type: ignore


@dataclass
class AngleCalc:
    v: geom.Vector
    deg: bool = False

    def __rich_repr__(self):
        yield "v", self.v
        yield "e0", self.e0
        yield "e1", self.e1
        yield "n_e0", self.n_e0
        yield "n_e1", self.n_e1
        yield "smallest_angle", self.smallest_angle
        yield "smallest_vector", self.smallest_vector_name
        yield "sign", self.sign

    @property
    def bases(self):
        return create_base_lines()

    @property
    def e0(self):
        return calc_angle_between_vectors(self.v, self.bases.e0.v, self.deg)

    @property
    def e1(self):
        return calc_angle_between_vectors(self.v, self.bases.e1.v, self.deg)

    @property
    def n_e0(self):
        return calc_angle_between_vectors(self.v, self.bases.n_e0.v, self.deg)

    @property
    def n_e1(self):
        return calc_angle_between_vectors(self.v, self.bases.n_e1.v, self.deg)

    @property
    def all_angles(self):
        return AngleResult(*[self.e0, self.e1, self.n_e0, self.n_e1])

    @property
    def smallest_angle(self):
        return self.all_angles.smallest.angle

    @property  # TODO -> this is a separate data structure.. -> want to have the angles as a named tuple that can find which one had the smallest angle.. or just return both ..
    def smallest_vector_name(self):
        return self.all_angles.smallest.vector_name

    @property
    def sign(self):
        y_component = float(self.v[1])  # type: ignore
        x_component = float(self.v[0])  # type: ignore
        print(-1 * x_component)
        print(-1* y_component)
        match self.smallest_vector_name:
            case "e0":
                return math.copysign(1, y_component)
            case "n_e0":
                return math.copysign(1, -1 * y_component)
            case "e1":
                return math.copysign(1, -1 * x_component)
            case "n_e1":
                return math.copysign(1, x_component)
            case _:
                raise Exception("invalid vector name")


if __name__ == "__main__":
    test_geom = create_test_lines()
