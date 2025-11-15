from polymap.examples.sample_updates import BottomLData
from polymap.geometry.update import update_domain, InvalidPolygonError
import pytest


def try_east0_move():
    return update_domain(BottomLData.domain, BottomLData.east_0, location_delta=1)


def test_east0_move_bad():
    with pytest.raises(InvalidPolygonError):
        update_domain(BottomLData.domain, BottomLData.east_0, location_delta=-8)


@pytest.mark.parametrize("surface", BottomLData.study_surfaces)
def test_outward_move(surface):
    update_domain(BottomLData.domain, surface, location_delta=0.5)
    assert 1


if __name__ == "__main__":
    d = try_east0_move()
    d.plot()
