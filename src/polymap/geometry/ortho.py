# from pipe import where, enumerate, map
from copy import deepcopy
from dataclasses import dataclass
from itertools import cycle

import shapely as sp
from utils4plans.geom import Coord, OrthoDomain
from utils4plans.lists import get_unique_one, pairwise

from polymap.geometry.surfaces import create_surface, index_surfaces
from polymap.geometry.vectors import (
    DirectionNames,
    is_perp_to_basis_vectors,
    vector_from_coords,
)
from polymap.interfaces import PairedCoord
from rich import print


def create_paired_coords(coords: list[Coord]):
    num_coords = len(coords)
    count = 0
    paired_coords: list[PairedCoord] = []
    for i, j in pairwise(cycle(coords)):
        paired_coords.append(PairedCoord(i, j))

        count += 1
        if count > num_coords - 2:
            break
    assert paired_coords[0].first == paired_coords[-1].last

    return paired_coords


# TODO => utils4plans
def find_and_replace_in_list(lst_: list, old: list, new: list):
    lst = deepcopy(lst_)
    assert len(new) == len(old)
    count = 0
    for ix, item in enumerate(lst):
        if item in old:
            lst[ix] = new[count]
            count += 1

    return lst


def find_and_replace_coords_in_list(
    original_coords: list[Coord],
    old_paired_coords: PairedCoord,
    new_paired_coords: PairedCoord,
):
    coords = find_and_replace_in_list(
        original_coords, old_paired_coords.as_list, new_paired_coords.as_list
    )
    coord_tuple = [i.as_tuple for i in coords]
    p = sp.Polygon(coord_tuple)
    if not p.is_valid:
        coords = find_and_replace_in_list(
            original_coords,
            old_paired_coords.as_list,
            list(reversed(new_paired_coords.as_list)),
        )
        return coords
    return coords


# def find_and_replace_coords_in_list(
#     original_coords: list[Coord],
#     old_paired_coords: list[Coord],
#     new_paired_coords: list[Coord],
# ):
#     oc = deepcopy(original_coords)
#     pass
#     # list(
#     #     original_coords
#     #     | where(lambda x: x in old_paired_coords)
#     #     | enumerate
#     #     | map(lambda x: a[x[0]])
#     # )


@dataclass
class FancyOrthoDomain(OrthoDomain):
    name: str = ""

    def __eq__(self, other: object) -> bool:
        if isinstance(other, FancyOrthoDomain):
            return (self.coords == other.coords) and (self.name == other.name)

        raise Exception(f"Invalid object of type {type(other)}")

    def __hash__(self) -> int:
        return hash(self.name) + sum([hash(i) for i in self.coords])

    # def __post_init__(self):
    #     assert self.is_orthogonal

    @classmethod
    def from_bounds(
        cls, minx: float, maxx: float, miny: float, maxy: float, name: str = ""
    ):
        coords = [(minx, miny), (maxx, miny), (maxx, maxy), (minx, maxy)]
        new_domain = cls([Coord(*i) for i in coords])
        new_domain.set_name(name)
        return new_domain

    @property
    def num_coords(self):
        return len(self.coords)

    @property
    def polygon(self):
        p = sp.Polygon(self.tuple_list)
        assert len(p.interiors) == 0, f"More than one interior: {p.interiors}"
        # assert p.is_valid, (
        #     f"Polygon not valid | name: {self.name} coords: {self.coords}"
        # )
        return p

    @property
    def centroid(self):
        centroid = self.polygon.centroid
        coords = [Coord(*i) for i in centroid.coords][0]
        return coords

    @property
    def normalized_coords(self):
        # NOTE: shapely will return coords in CW direction starting from the bottom left
        return [Coord(*i) for i in self.polygon.exterior.normalize().coords]

    @property
    def paired_coords(self):
        return create_paired_coords(self.normalized_coords)

    @property
    def vectors(self):
        return [vector_from_coords(*i) for i in self.paired_coords]

    @property
    def is_orthogonal(self):
        res = [is_perp_to_basis_vectors(i) for i in self.vectors]
        return all(res)

    @property
    def surfaces(self):
        # print(self.name, self.vectors)
        surfaces = [
            create_surface(i, j, self.name)
            for i, j in zip(
                self.vectors,
                self.paired_coords,
            )
        ]
        return index_surfaces(surfaces)

    @property
    def substantial_surfaces(self):
        if len(self.surfaces) > 4:
            return list(filter(lambda x: not x.is_small, self.surfaces))
        else:
            return self.surfaces

    @property
    def summarize_surfaces(self):
        print(self.name)
        for i in sorted(self.substantial_surfaces, key=lambda surf: surf.direction):
            print(f"{i.name:<20} | {i.range.size:.2f}")

    def get_surface(self, direction_name: DirectionNames, direction_ix: int = 0):
        return get_unique_one(
            self.surfaces,
            lambda x: (x.direction.name == direction_name)
            and (x.direction_ix == direction_ix),
        )

    def get_surface_by_name(self, surf_name: str):
        return get_unique_one(self.surfaces, lambda x: str(x) == surf_name)

    def set_name(self, name: str):
        self.name = name

    # def get_range_by_axis(self, axis: Axes):
    #     bounds = ShapelyBounds(*self.shapely_polygon.bounds)
    #     if axis == "X":
    #         return FancyRange(bounds.minx, bounds.maxx)
    #     else:
    #         return FancyRange(bounds.miny, bounds.maxy)
    #
