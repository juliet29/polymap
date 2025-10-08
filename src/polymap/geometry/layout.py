from dataclasses import dataclass

import shapely as sp
from rich import print
from pipe import where, groupby, take, select, map, sort

from utils4plans.lists import chain_flatten, get_unique_one, sort_and_group_objects
from utils4plans.sets import set_difference

from polymap.examples.layout import layout as sample_layout
from polymap.geometry.ortho import FancyOrthoDomain
from polymap.geometry.surfaces import Surface, FancyRange
from polymap.interfaces import CoordsType
from polymap.visuals import plot_polygon
from polymap.geometry.vectors import Axes


@dataclass
class Layout:
    domains: list[FancyOrthoDomain]
    # post init -> assert names are unique!

    def plot_layout(self):
        polygons = sp.MultiPolygon([i.shapely_polygon for i in self.domains])
        plot_polygon(polygons)

    def get_domain(self, name):
        return get_unique_one(self.domains, lambda x: x.name == name)

    @property
    def surfaces(self):
        return chain_flatten([i.surfaces for i in self.domains])

    def get_other_surfaces(self, surf: Surface):
        return set_difference(self.surfaces, [surf])


def create_layout(layout: dict[str, CoordsType]):
    domains: list[FancyOrthoDomain] = []
    for k, v in layout.items():
        domain = FancyOrthoDomain.from_tuple_list(v)
        domain.set_name(k)
        domains.append(domain)

    return Layout(domains)


def get_candidate_surface_neighbors(layout: Layout, surf: Surface):
    def best_surface_for_each_domain(surfs: list[Surface]):
        best_surfs = []
        res = sort_and_group_objects(surfs, lambda x: x.domain_name)
        for group in res:
            sort_surfs = sorted(group, key=lambda x: x.location, reverse=True)
            best_surfs.append(sort_surfs[0])
        return best_surfs

    res = list(
        layout.get_other_surfaces(surf)
        | where(lambda x: x.axis == surf.axis)
        | where(lambda x: surf.range.is_coincident(x.range))
        | where(lambda x: x.location <= surf.location)
    )

    print(res)

    res2 = best_surface_for_each_domain(res)

    print(f"candidate nbs for {surf}")

    print(res2)


if __name__ == "__main__":
    layout = create_layout(sample_layout)
    # print(layout.get_domain("yellow_rect").surfaces)
    surf = layout.get_domain("red_l").get_surface("south", 1)
    get_candidate_surface_neighbors(layout, surf)
