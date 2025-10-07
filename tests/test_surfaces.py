from polymap.examples.sample_domains import ortho_coords
from utils4plans.geom import Coord
from polymap.geometry.ortho import create_paired_coords
from polymap.geometry.vectors import CardinalDirections as CD
from rich import print
from polymap.geometry.surfaces import Surface, index_surfaces


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


if __name__ == "__main__":
    test_index_surfaces()
