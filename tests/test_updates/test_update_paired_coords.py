from utils4plans.geom import Coord
import pytest
import geom

from polymap.examples.sample_updates import BottomLData
from polymap.geometry.modify.update import (
    UpdateCoordsInfo,
    create_update_coords_tuple,
    UpdateCoordsTuple,
)
from polymap.geometry.paired_coords import PairedCoord
from rich import print  # type:ignore

PairedCoordUpdateResult = tuple[PairedCoord, PairedCoord, PairedCoord]


def check_indices_are_aligned(
    res: list[PairedCoord], expected_new_: PairedCoordUpdateResult
):
    expected_new = list(expected_new_)
    first_to_occur = expected_new[0]
    ix_of_first = res.index(first_to_occur)

    n_items_to_match = len(expected_new)
    slice_to_match = slice(ix_of_first, ix_of_first + n_items_to_match)
    assert res[slice_to_match] == expected_new


def check_updated_coords_match(
    paired_coords: list[PairedCoord],
    target: PairedCoord,
    v: geom.Vector,
    expected_coords: UpdateCoordsTuple,
):

    res = create_update_coords_tuple(paired_coords, target, v)
    print(f"{res=}")
    print(f"{expected_coords=}")
    assert res == expected_coords


def check_ok(
    paired_coords, target, v, expected_new: PairedCoordUpdateResult, start_ix: int
):
    n_coords = len(paired_coords)
    info_list = [
        UpdateCoordsInfo(coord, (ix + start_ix) % n_coords)
        for ix, coord in enumerate(expected_new)
    ]
    expected_tuple = UpdateCoordsTuple(*info_list)
    res = check_updated_coords_match(paired_coords, target, v, expected_tuple)
    # check_indices_are_aligned(res, expected_new)


class TestUpdatingPairedCoords(BottomLData):

    def test_moving_east0_out(self):
        v = geom.Vector([3, 0])
        target = self.east_0.coords

        # these are given in order of appearance!
        expected_new = (
            PairedCoord(Coord(3, 2), Coord(5, 2)),
            PairedCoord(Coord(5, 2), Coord(5, 1)),
            PairedCoord(Coord(5, 1), Coord(1, 1)),
        )
        start_ix = 3

        check_ok(self.paired_coords, target, v, expected_new, start_ix)

    def test_moving_east1_in(self):
        v = geom.Vector([-1, 0])
        target = self.east_1.coords

        expected_new = (
            PairedCoord(Coord(1, 3), Coord(2, 3)),
            PairedCoord(Coord(2, 3), Coord(2, 2)),
            PairedCoord(Coord(2, 2), Coord(2, 2)),
        )
        start_ix = 1

        check_ok(self.paired_coords, target, v, expected_new, start_ix)

    def test_moving_north0_out(self):
        v = geom.Vector([0, 1])
        target = self.north_0.coords

        expected_new = (
            PairedCoord(Coord(1, 1), Coord(1, 4)),
            PairedCoord(Coord(1, 4), Coord(3, 4)),
            PairedCoord(Coord(3, 4), Coord(3, 2)),
        )
        start_ix = 0

        check_ok(self.paired_coords, target, v, expected_new, start_ix)

    def test_moving_west0_in(self):
        v = geom.Vector([-1, 0])
        target = self.west_0.coords
        print(f"{target=}")

        expected_new = (
            PairedCoord(Coord(2, 1), Coord(0, 1)),
            PairedCoord(Coord(0, 1), Coord(0, 3)),
            PairedCoord(Coord(0, 3), Coord(3, 3)),
        )
        start_ix = 5

        check_ok(self.paired_coords, target, v, expected_new, start_ix)

    def test_moving_south0_out(self):
        v = geom.Vector([0, -1])
        target = self.south_0.coords
        print(f"{str(target)=}")

        expected_new = (
            PairedCoord(Coord(2, 2), Coord(2, 0)),
            PairedCoord(Coord(2, 0), Coord(1, 0)),
            PairedCoord(Coord(1, 0), Coord(1, 3)),
        )
        start_ix = 4

        check_ok(self.paired_coords, target, v, expected_new, start_ix)

    def test_non_orthog_vector(self):
        v = geom.Vector([1, 0])
        target = self.south_0.coords
        with pytest.raises(AssertionError):
            create_update_coords_tuple(self.paired_coords, target, v)


if __name__ == "__main__":
    t = TestUpdatingPairedCoords()
    t.test_moving_west0_in()
