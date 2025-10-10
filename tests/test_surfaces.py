from polymap.examples.sample_domains import ortho_coords
from utils4plans.geom import Coord
from polymap.geometry.ortho import create_paired_coords
from polymap.geometry.vectors import CardinalDirections as CD
from polymap.geometry.vectors import Axes
from rich import print
from polymap.geometry.surfaces import (
    Surface,
    index_surfaces,
    FancyRange,
    coords_to_location,
    coords_to_range,
)
import pytest
from polymap.interfaces import PairedCoord
from utils4plans.sets import set_difference


sample_paired_coords = PairedCoord(Coord(1, 0), Coord(2, 0))


def create_test_surfaces():
    coords = [Coord(*i) for i in ortho_coords["BOTTOM_UP_L"]]
    coords.append(Coord(*ortho_coords["BOTTOM_UP_L"][0]))
    paired_coords = create_paired_coords(coords)
    # print(paired_coords)
    directions = reversed([CD.WEST, CD.NORTH, CD.EAST, CD.SOUTH, CD.EAST, CD.SOUTH])
    # print(list(directions))
    return [Surface(drn, coord, "") for drn, coord in zip(directions, paired_coords)]


def test_index_surfaces():
    surfs = create_test_surfaces()
    res = index_surfaces(surfs)
    south_ixs = [i.direction_ix for i in res if i.direction.name == "south"]
    assert set(south_ixs) == set([0, 1])
    north_ixs = [i.direction_ix for i in res if i.direction.name == "north"]
    assert set(north_ixs) == set([0])


coord_test: list[tuple[Axes, PairedCoord, FancyRange, int]] = [
    ("X", PairedCoord(Coord(1, 0), Coord(2, 0)), FancyRange(1, 2), 0),
    ("Y", PairedCoord(Coord(1, 10), Coord(1, 20)), FancyRange(10, 20), 1),
]


@pytest.mark.parametrize("ax, coord, range, location", coord_test)
def test_coord_conversion(ax, coord, range, location):
    assert range == coords_to_range(coord, ax)
    assert location == coords_to_location(coord, ax)


def test_surface_equality():
    a = Surface(CD.NORTH, sample_paired_coords, "")
    b = Surface(CD.NORTH, sample_paired_coords, "")
    assert a == b


def test_surface_inequality():
    a = Surface(CD.NORTH, sample_paired_coords, "")
    b = Surface(CD.SOUTH, sample_paired_coords, "test")
    assert a != b


def test_coords_set():
    surfs = create_test_surfaces()
    new_surf = Surface(CD.SOUTH, sample_paired_coords, "test")
    all_surfs = surfs + [new_surf]
    res = set_difference(all_surfs, [new_surf])
    assert len(res) == len(surfs)


def test_update_surface():
    a = Surface(CD.NORTH, sample_paired_coords, "")
    new_surf = a.update_surface_location(3)
    assert new_surf.location == a.coords[0].y + 3


if __name__ == "__main__":
    test_coords_set()
