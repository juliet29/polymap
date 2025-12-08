import geom
import math


def calc_angle_between_vectors(v1: geom.Vector, v2: geom.Vector, deg=False):
    # TODO: that have this twice -> one is in rotate, so thould bring together..
    def clip_value(value, lower_bound=-1, upper_bound=1):
        return max(lower_bound, min(value, upper_bound))

    v1mag = abs(v1)
    v2mag = abs(v2)
    assert (
        v1mag > 0 and v2mag > 0
    ), f"one of vectors has magnitude less than or equal to 0: {v1}, {v2}"

    cos_theta = v1.dot(v2) / (v1mag * v2mag)
    assert (
        cos_theta >= -1 and cos_theta <= 1
    ), f"cos_theta `{cos_theta}` should be -1 <= cos_theta <= 1"

    theta = math.acos(clip_value(cos_theta))
    if deg:
        return math.degrees(theta)

    return theta  # TODO want to round this ideally..
