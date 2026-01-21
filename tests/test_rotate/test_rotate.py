from polymap.examples.msd import get_oneoff_msd_plan
from polymap.rotate.main import rotate_layout
from math import degrees
import pytest


@pytest.mark.skip("Add more test cases here")
def test_rotate_example_layout():
    pass


@pytest.mark.filterwarnings(
    "ignore:.*divide by zero encountered in oriented_envelope.*"
)
def test_rotate_oneoff_layout():
    layout = get_oneoff_msd_plan()
    angle, _ = rotate_layout(
        layout
    )  # TODO: figure why getting divide by 0 warning here.. .
    assert degrees(angle) == 0


if __name__ == "__main__":
    pass
