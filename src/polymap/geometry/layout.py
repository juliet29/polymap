from dataclasses import dataclass

import shapely as sp
from rich import print
from pipe import where, groupby, take, select, map, sort

from utils4plans.lists import (
    chain_flatten,
    get_unique_one,
    sort_and_group_objects,
    pairwise,
)
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


def create_layout_from_dict(
    layout: dict[str, CoordsType],
):  # TODO: CoordsType is a misnomer
    domains: list[FancyOrthoDomain] = []
    for k, v in layout.items():
        domain = FancyOrthoDomain.from_tuple_list(v)
        domain.set_name(k)
        domains.append(domain)

    return Layout(domains)


def get_candidate_surface_neighbors(layout: Layout, surf: Surface):
    # SPlit into three functions and move elsewhere -> no longer just geometry
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

    return best_surface_for_each_domain(res)


def filter_candidate_neighbors(
    layout: Layout, surf: Surface, other_surfs: list[Surface]
):
    sorted_surfs = sorted(
        other_surfs,
        key=lambda x: x.location,
    )  # from lowest to highest.. -> from furthest away to closest to the current surf..
    bad_surfs = []

    for further_surf, closer_surf in pairwise(sorted_surfs):
        closer_domain = layout.get_domain(closer_surf.domain_name)
        domain_range = closer_domain.get_range_by_axis(closer_surf.normal_axis)

        surf_range = FancyRange(further_surf.location, surf.location)
        if surf_range.contains(domain_range):
            print(
                f"`{closer_domain.name}` is contained in the distance betwen the current surf `{surf}` and the further surf on `{further_surf.domain_name}`. Removing the further surf"
            )
            bad_surfs.append(further_surf)
    remaining = set_difference(other_surfs, bad_surfs)
    print(remaining)
    return remaining


if __name__ == "__main__":
    layout = create_layout_from_dict(sample_layout)
    # print(layout.get_domain("yellow_rect").surfaces)
    surf = layout.get_domain("red_l").get_surface("south", 1)
    os = get_candidate_surface_neighbors(layout, surf)
    filter_candidate_neighbors(layout, surf, os)
