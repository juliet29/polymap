from polymap.geometry.ortho import FancyOrthoDomain
from typing import Literal

CoordsType = list[tuple[float | int, float | int]]
OrthoNames = Literal["L", "BOTTOM_UP_L", "NON_ORTHO", "SQUARE"]

ortho_coords: dict[OrthoNames, CoordsType] = {
    "L": [],
    "BOTTOM_UP_L": [(1, 1), (2, 1), (2, 2), (3, 2), (3, 3), (1, 3)],
    "NON_ORTHO": [(1, 1), (2, 2), (3, 2), (3, 3), (1, 3)],
    "SQUARE": [
        (0, 0),
        (1, 0),
        (1, 1),
        (0, 1),
    ],
}


def create_ortho_domain(key: OrthoNames = "BOTTOM_UP_L"):
    return FancyOrthoDomain.from_tuple_list(ortho_coords[key])
