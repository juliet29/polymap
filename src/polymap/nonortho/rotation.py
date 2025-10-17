from polymap.nonortho.interfaces import create_base_lines, ORIGIN
from dataclasses import dataclass
from polymap.geometry.vectors import vector_to_sp_line, sp_line_to_vector
import geom
import math
import shapely as sp
from typing import NamedTuple, Literal


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
        yield "smallest_vector", self.closest_vector_name
        yield "sign", self.sign

    @property
    def summary(self):
        return f"{self.v} is {'+' if self.sign > 0 else '-'}{self.smallest_angle:.2f}deg/rad away from the {self.closest_vector_name} axis"

    @property
    def bases(self):
        return create_base_lines()

    # TODO -> this could be a dict.. or another class..
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

    @property
    def closest_vector_name(self):
        return self.all_angles.smallest.vector_name

    @property
    def sign(self):
        y_component = float(self.v[1])  # type: ignore
        x_component = float(self.v[0])  # type: ignore
        # TODO: add to README explaining logic..
        match self.closest_vector_name:
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


def move_vector(v: geom.Vector):
    angle_info = AngleCalc(v)
    line = vector_to_sp_line(v)
    rotation_angle = -1 * angle_info.sign * angle_info.smallest_angle
    new_line = sp.affinity.rotate(line, rotation_angle, origin=ORIGIN, use_radians=True)
    return sp_line_to_vector(new_line)
