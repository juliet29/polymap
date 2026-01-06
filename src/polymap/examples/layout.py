from polymap.interfaces import CoordsType

green_north = 3.9
pink_north = 3.8

layout_coords: dict[str, CoordsType] = {
    "blue": [(1, 1), (4, 1), (4, 2), (1, 2)],
    "yellow": [(1, 2.1), (2, 2.1), (2, 3), (1, 3)],
    "green": [
        (2.1, 2.2),
        (4, 2.2),
        (4, 3.1),
        (3, 3.1),
        (3, green_north),
        (2.1, green_north),
    ],
    "pink": [(3.1, 3.3), (4, 3.3), (4, pink_north), (3.1, pink_north)],
    "red": [(1, 3.1), (2, 3.1), (2, 4), (4, 4), (4, 5), (1, 5), (1, 3.1)],
}

example_layouts = [layout_coords]
