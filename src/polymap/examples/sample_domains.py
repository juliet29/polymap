from polymap.geometry.ortho import FancyOrthoDomain
from typing import Literal

CoordsType = list[tuple[float | int, float | int]]
OrthoNames = Literal["L", "BOTTOM_UP_L"]

ortho_coords: dict[OrthoNames, CoordsType] = {
    "L": [],
    "BOTTOM_UP_L": [(1, 1), (2, 1), (2, 2), (3, 2), (3, 3), (1, 3)],
}


def create_ortho_domain(key: OrthoNames = "BOTTOM_UP_L"):
    return FancyOrthoDomain.from_tuple_list(ortho_coords[key])
