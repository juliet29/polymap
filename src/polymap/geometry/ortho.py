# from pipe import where, enumerate, map
from dataclasses import dataclass

import shapely as sp
from utils4plans.geom import Coord, OrthoDomain
from utils4plans.lists import get_unique_one

from polymap.geometry.paired_coords import PairedCoord, create_paired_coords
from polymap.geometry.surfaces import create_surface, index_surfaces
from polymap.geometry.vectors import (
    DirectionNames,
    is_perp_to_basis_vectors,
    pretty_print_vector,
    vector_from_coords,
)
from rich import print


@dataclass
class FancyOrthoDomain(OrthoDomain):

    def __eq__(self, other: object) -> bool:
        if isinstance(other, FancyOrthoDomain):
            return (self.coords == other.coords) and (self.name == other.name)

        raise Exception(f"Invalid object of type {type(other)}")

    def __hash__(self) -> int:
        return hash(self.name) + sum([hash(i) for i in self.coords])

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
    def paired_coords(self) -> list[PairedCoord]:
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

    def summarize_surfaces(self, sort=False, substantial=False):
        # NOTE: this ignores small surfaces!
        #
        print(self.name)
        if sort and substantial:
            for i in sorted(self.substantial_surfaces, key=lambda surf: surf.direction):
                print(f"{i.name_w_domain:<20} | {i.range.size:.2f}")
        else:
            for i in self.surfaces:
                print(f"{i.name_w_domain:<20} | {i.range.size:.4f}")

    @property
    def create_vector_summary(self):
        lst = []
        for ix, i in enumerate(self.vectors):
            if is_perp_to_basis_vectors(i):
                lst.append(f"{ix:>3}| {pretty_print_vector(i)}")
            else:
                lst.append(f"{ix:>3}| {i} | NOT ORTHO")
        return lst

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
