from polymap.interfaces import CoordsType
from polymap.geometry.ortho import FancyOrthoDomain

layout: dict[str, CoordsType] = {
    "blue": [(1, 1), (4, 1), (4, 2), (1, 2)],
    "yellow": [(1, 2.1), (2, 2.1), (2, 3), (1, 3)],
    "green": [(2.1, 2.2), (4, 2.2), (4, 3.1), (3, 3.1), (3, 3.9), (2.1, 3.9)],
    "pink": [(3.1, 3.3), (4, 3.3), (4, 3.8), (3.1, 3.8)],
    "red": [(1, 3.1), (2, 3.1), (2, 4), (4, 4), (4, 5), (1, 5), (1, 3.1)],
}
