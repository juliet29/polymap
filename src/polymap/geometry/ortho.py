from utils4plans.geom import OrthoDomain, Coord
from dataclasses import dataclass
import shapely as sp
from utils4plans.lists import pairwise
from rich import print
from itertools import cycle

from polymap.geometry.vectors import vector_from_coords, is_perp_to_basis_vectors
from polymap.interfaces import PairedCoord
from polymap.geometry.surfaces import vector_to_surface, index_surfaces


def create_paired_coords(coords: list[Coord]):
    num_coords = len(coords)
    count = 0
    paired_coords: list[PairedCoord] = []
    for i, j in pairwise(cycle(coords)):
        paired_coords.append(PairedCoord(i, j))
        # print(f"{count}: {i}, {j}")

        count += 1
        if count > num_coords - 2:
            break
    assert paired_coords[0].a == paired_coords[-1].b

    return paired_coords


@dataclass
class FancyOrthoDomain(OrthoDomain):
    name: str = ""

    # TODO want to do some checks, make sure is closed and valid..
    @property
    def num_coords(self):
        return len(self.coords)

    @property
    def shapely_polygon(self):
        p = sp.Polygon(self.tuple_list)
        assert len(p.interiors) == 0, f"More than one interior: {p.interiors}"
        assert p.is_valid, "Polygon not valid"
        return p

    @property
    def normalized_coords(self):
        # NOTE: shapely will return coords in CW direction starting from the bottom left
        return [Coord(*i) for i in self.shapely_polygon.exterior.normalize().coords]

    @property
    def paired_coords(self):
        return create_paired_coords(self.normalized_coords)

        # count = 0
        # paired_coords: list[PairedCoord] = []

        # for i, j in pairwise(cycle(self.normalized_coords)):
        #     paired_coords.append(PairedCoord(i, j))
        #     print(f"{count}: {i}, {j}")

        #     count += 1
        #     if count > self.num_coords - 1:
        #         break
        # assert paired_coords[0].a == paired_coords[-1].b

        # return paired_coords

    @property
    def vectors(self):
        return [vector_from_coords(*i) for i in self.paired_coords]

    @property
    def is_orthogonal(self):
        res = [is_perp_to_basis_vectors(i) for i in self.vectors]
        return all(res)  # TODO: on post init...

    @property
    def surfaces(self):
        surfaces = [
            vector_to_surface(i, j, self.name)
            for i, j in zip(
                self.vectors,
                self.paired_coords,
            )
        ]
        return index_surfaces(surfaces)

    def set_name(self, name: str):
        self.name = name
