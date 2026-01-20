from typing import NamedTuple
from polymap.examples.domains import create_ortho_domain
from polymap.examples.sample_updates import BottomLData
from polymap.geometry.modify.update import update_domain, InvalidPolygonError, Move
import pytest
from polymap.geometry.vectors import CardinalDirections, Direction


def try_east0_move():
    return update_domain(Move(BottomLData.domain, BottomLData.east_0, delta=1))


def test_east0_move_bad():
    with pytest.raises(InvalidPolygonError):
        update_domain(Move(BottomLData.domain, BottomLData.east_0, delta=-8))


@pytest.mark.parametrize("surface", BottomLData.study_surfaces)
def test_outward_move(surface):
    update_domain(Move(BottomLData.domain, surface, delta=0.5))
    assert 1


class CompareMove(NamedTuple):
    delta: float
    new_loc: float


high_plus = CompareMove(0.1, 1.1)
high_minus = CompareMove(-0.1, 0.9)

low_plus = CompareMove(0.1, 0.1)
low_minus = CompareMove(-0.1, -0.1)

square_moves: list[tuple[Direction, CompareMove]] = [
    (CardinalDirections.NORTH, high_plus),
    (CardinalDirections.NORTH, high_minus),
    (CardinalDirections.EAST, high_plus),
    (CardinalDirections.EAST, high_minus),
    # lows
    (CardinalDirections.SOUTH, low_plus),
    (CardinalDirections.SOUTH, low_plus),
    (CardinalDirections.WEST, low_plus),
    (CardinalDirections.WEST, low_plus),
]


@pytest.mark.parametrize("drn, compare_move", square_moves)
def test_moves_on_square(drn: Direction, compare_move: CompareMove):
    delta, new_loc = compare_move
    domain = create_ortho_domain("SQUARE")
    surface = domain.get_surface(drn.name)
    move = Move(domain, surface, delta)

    new_domain = update_domain(move)
    new_surf = new_domain.get_surface(drn.name)
    assert new_surf.location == new_loc


if __name__ == "__main__":
    d = try_east0_move()
