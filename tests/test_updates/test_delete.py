from utils4plans.geom import Coord
from rich import print
from polymap.examples.domains import create_ortho_domain
from polymap.geometry.modify.delete import Delete, delete_paired_coords
from polymap.geometry.ortho import create_paired_coords
from polymap.geometry.paired_coords import PairedCoord


def test_delete_on_square():
    domain = create_ortho_domain("SQUARE")

    pcs = [i.coords for i in domain.surfaces]
    surface = domain.get_surface("north")
    delete = Delete(pcs, surface.coords)
    new_coords = delete_paired_coords(delete)
    assert len(new_coords) == len(pcs) - 1


def test_delete_on_square_with_north_inner():
    # domain = create_ortho_domain("SQUARE_EXTRA_INNER")
    bad_pc = PairedCoord(Coord(0.5, 1), Coord(0.5, 0.5))
    input_coords = [(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)]
    coords = map(lambda x: Coord(*x), input_coords)
    pcs = create_paired_coords(list(coords))
    # pcs.insert()
    for ix, pc in enumerate(pcs):
        print(f"{ix}: {str(pc)}")

    # surface = domain.get_surface("north")
    # delete = Delete(pcs, surface)
    # new_coords = delete_paired_coords(delete)
    # assert len(new_coords) == len(pcs) - 1


if __name__ == "__main__":
    test_delete_on_square_with_north_inner()
