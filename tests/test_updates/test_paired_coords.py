from utils4plans.geom import Coord
from utils4plans.sets import set_difference, set_equality
from polymap.examples.sample_domains import create_ortho_domain
import geom

from polymap.geometry.update import update_paired_coords
from polymap.interfaces import PairedCoord
from rich import print

PairedCoordUpdateResult = tuple[PairedCoord, PairedCoord, PairedCoord]
l_dom = create_ortho_domain("BOTTOM_UP_L")
square = create_ortho_domain("SQUARE")


def check_updated_coords_match(
    paired_coords: list[PairedCoord],
    target: PairedCoord,
    v: geom.Vector,
    expected_coords: PairedCoordUpdateResult,
):
    res = update_paired_coords(paired_coords, target, v)

    removed = set_difference(paired_coords, res)
    new = set_difference(res, paired_coords)
    assert len(removed) == len(new)
    assert set_equality(new, list(expected_coords))

    return res


def check_indices_are_aligned(
    res: list[PairedCoord], expected_new_: PairedCoordUpdateResult
):
    expected_new = list(expected_new_)
    first_to_occur = expected_new[0]
    ix_of_first = res.index(first_to_occur)

    n_items_to_match = len(expected_new)
    slice_to_match = slice(ix_of_first, ix_of_first + n_items_to_match)
    assert res[slice_to_match] == expected_new


class TestUpdatingBottomL:
    domain = create_ortho_domain("BOTTOM_UP_L")
    paired_coords = domain.paired_coords

    # targets
    east_0 = domain.get_surface("east", 0).coords
    east_1 = domain.get_surface("east", 1).coords

    def test_moving_east0_out(self):
        v = geom.Vector([3, 0])
        target = self.east_0

        expected_new = (
            PairedCoord(first=Coord(x=3.0, y=2.0), last=Coord(x=5.0, y=2.0)),
            PairedCoord(first=Coord(x=5.0, y=2.0), last=Coord(x=5.0, y=1.0)),
            PairedCoord(first=Coord(x=5.0, y=1.0), last=Coord(x=1.0, y=1.0)),
        )
        res = check_updated_coords_match(self.paired_coords, target, v, expected_new)
        check_indices_are_aligned(res, expected_new)

    def test_moving_east1_in(self):
        v = geom.Vector([-1, 0])
        target = self.east_1

        # this should be given in order of appearance.., then search for subsequence
        expected_new = (
            PairedCoord(first=Coord(x=1.0, y=3.0), last=Coord(x=2.0, y=3.0)),
            PairedCoord(first=Coord(x=2.0, y=3.0), last=Coord(x=2.0, y=2.0)),
            PairedCoord(first=Coord(x=2.0, y=2.0), last=Coord(x=2.0, y=2.0)),
        )

        res = check_updated_coords_match(self.paired_coords, target, v, expected_new)

        check_indices_are_aligned(res, expected_new)


if __name__ == "__main__":
    t = TestUpdatingBottomL()
    print(t.paired_coords)
    t.test_moving_east1_in()
