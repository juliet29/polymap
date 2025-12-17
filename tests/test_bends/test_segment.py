from utils4plans.geom import Coord
from polymap.bends.generate import segment_coords_center, segment_coords_end
from polymap.interfaces import PairedCoord


def test_segment_coords_x():
    a1 = Coord(0, 0)
    a2 = Coord(1, 0)
    coords = PairedCoord(a1, a2)

    b1 = Coord(0.5, 0)
    b2 = Coord(0.6, 0)
    expected = (a1, b1, b2, a2)

    res = segment_coords_center(coords, "X", 0.1)
    assert expected == res


def test_segment_coords_y():
    a1 = Coord(0, 0)
    a2 = Coord(0, 1)
    coords = PairedCoord(a1, a2)

    b1 = Coord(0, 0.5)
    b2 = Coord(0, 0.6)
    expected = (a1, b1, b2, a2)

    res = segment_coords_center(coords, "Y", 0.1)
    assert expected == res


def test_segment_coords_end_x():
    a1 = Coord(0, 0)
    a2 = Coord(1, 0)
    coords = PairedCoord(a1, a2)
    b1 = Coord(0.9, 0)
    expected = (a1, b1, a2)

    res = segment_coords_end(coords, "X", 0.1)
    assert expected == res


def test_segment_coords_end_y():
    a1 = Coord(0, 0)
    a2 = Coord(0, 1)
    coords = PairedCoord(a1, a2)
    b1 = Coord(0, 0.9)
    expected = (a1, b1, a2)

    res = segment_coords_end(coords, "Y", 0.1)
    assert expected == res


if __name__ == "__main__":
    test_segment_coords_end_x()
