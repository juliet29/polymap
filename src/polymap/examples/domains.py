from utils4plans.geom import CoordsType
from polymap.geometry.ortho import FancyOrthoDomain
from typing import Literal

OrthoNames = Literal[
    "BOTTOM_UP_L",
    "NON_ORTHO",
    "SQUARE",
    "NON_ORTHO_SQUARE",
    "SQUARE_W_EXTRA_POINTS",
    "SQUARE_EXTRA_WEST",
    "SQUARE_EXTRA_NORTH_WEST",
    "SQUARE_EXTRA_INNER",
    "SQUARE_TRI",
    "SQUARE_2TRI",
]

ortho_coords: dict[OrthoNames, CoordsType] = {
    "BOTTOM_UP_L": [(1, 1), (2, 1), (2, 2), (3, 2), (3, 3), (1, 3)],
    "NON_ORTHO": [(1, 1), (2, 2), (3, 2), (3, 3), (1, 3)],
    "SQUARE": [
        (0, 0),
        (1, 0),
        (1, 1),
        (0, 1),
    ],
    "NON_ORTHO_SQUARE": [(0, 0), (1, 0.1), (0.8, 1), (0, 1)],
    "SQUARE_W_EXTRA_POINTS": [
        (0, 0),
        (1, 0),
        (1, 1),
        (0.5, 1),
        (0, 1),
    ],
    "SQUARE_EXTRA_WEST": [(0, 0), (1, 0), (1, 1), (0, 1), (0, 0.5)],
    "SQUARE_EXTRA_NORTH_WEST": [(0, 0), (1, 0), (1, 1), (0.5, 1), (0, 1), (0, 0.5)],
    "SQUARE_EXTRA_INNER": [
        (0, 0),
        (1, 0),
        (1, 1),
        (0.5, 0.5),
        (0, 1),
    ],
    "SQUARE_TRI": [(0, 3), (3, 3), (7, 0), (0, 0)],
    "SQUARE_2TRI": [
        (0, 6),
        (3, 6),
        (7, 3),
        (3, 0),
        (0, 0),
    ],
}


def create_ortho_domain(key: OrthoNames = "BOTTOM_UP_L"):
    return FancyOrthoDomain.from_tuple_list(ortho_coords[key])
