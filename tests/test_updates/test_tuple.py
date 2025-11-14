from utils4plans.geom import Coord
from polymap.examples.sample_domains import create_ortho_domain
import geom

from polymap.geometry.update import (
    UpdateCoordsInfo,
    create_update_coords_tuple,
    UpdateCoordsTuple,
)
from polymap.interfaces import PairedCoord

PairedCoordUpdateResult = tuple[PairedCoord, PairedCoord, PairedCoord]
l_dom = create_ortho_domain("BOTTOM_UP_L")
square = create_ortho_domain("SQUARE")


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
    assert res == expected_coords
    print(res)
    print(expected_coords)


def check_ok(
    paired_coords, target, v, expected_new: PairedCoordUpdateResult, start_ix: int
):
    info_list = [
        UpdateCoordsInfo(coord, ix + start_ix) for ix, coord in enumerate(expected_new)
    ]
    expected_tuple = UpdateCoordsTuple(*info_list)
    res = check_updated_coords_match(paired_coords, target, v, expected_tuple)
    # check_indices_are_aligned(res, expected_new)


class TestUpdatingBottomL:
    domain = create_ortho_domain("BOTTOM_UP_L")
    paired_coords = domain.paired_coords

    # targets
    east_0 = domain.get_surface("east", 0).coords
    east_1 = domain.get_surface("east", 1).coords
    north_0 = domain.get_surface("north", 0).coords
    west_0 = domain.get_surface("west", 0).coords

    def test_moving_east0_out(self):
        v = geom.Vector([3, 0])
        target = self.east_0

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
        target = self.east_1

        expected_new = (
            PairedCoord(Coord(1, 3), Coord(2, 3)),
            PairedCoord(Coord(2, 3), Coord(2, 2)),
            PairedCoord(Coord(2, 2), Coord(2, 2)),
        )
        start_ix = 1

        check_ok(self.paired_coords, target, v, expected_new, start_ix)

    def test_moving_north0_out(self):
        v = geom.Vector([0, 1])
        target = self.north_0

        expected_new = (
            PairedCoord(Coord(1, 1), Coord(1, 4)),
            PairedCoord(Coord(1, 4), Coord(3, 4)),
            PairedCoord(Coord(3, 4), Coord(3, 2)),
        )
        start_ix = 0

        check_ok(self.paired_coords, target, v, expected_new, start_ix)

    def test_moving_west0_in(self):
        v = geom.Vector([0, -1])
        target = self.west_0

        expected_new = (
            PairedCoord(Coord(2, 1), Coord(0, 1)),
            PairedCoord(Coord(0, 1), Coord(0, 3)),
            PairedCoord(Coord(0, 3), Coord(3, 3)),
        )
        start_ix = -1

        check_ok(self.paired_coords, target, v, expected_new, start_ix)


if __name__ == "__main__":
    t = TestUpdatingBottomL()
    t.test_moving_west0_in()
