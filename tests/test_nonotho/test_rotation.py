import pytest
import geom
from polymap.nonortho.rotation import BaseVectorNames, create_test_lines, AngleCalc
import numpy as np

test_lines = create_test_lines()


angle_data: list[tuple[geom.Vector, BaseVectorNames, float, int]] = [
    (test_lines.e0.a10.v, "e0", 10, 1),
    (test_lines.e0.n_a10.v, "e0", 10, -1),
    (test_lines.n_e0.a10.v, "n_e0", 10, 1),
    (test_lines.n_e0.n_a10.v, "n_e0", 10, -1),
    # e1
    (test_lines.e1.a10.v, "e1", 10, 1),
    (test_lines.e1.n_a10.v, "e1", 10, -1),
    (test_lines.n_e1.a10.v, "n_e1", 10, 1),
    (test_lines.n_e1.n_a10.v, "n_e1", 10, -1),
]


@pytest.mark.parametrize("v, closest_vector, angle, sign", angle_data)
def test_angle_calc(v, closest_vector, angle, sign):
    a = AngleCalc(v, deg=True)
    assert a.smallest_vector_name == closest_vector
    assert np.isclose(a.smallest_angle, angle)
    assert a.sign == sign

if __name__ == "__main__":
   test_lines = create_test_lines()
   v =test_lines.e0.a10.v 
   a = AngleCalc(v, deg=True) 