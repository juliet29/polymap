from rich import print
from pipe import where

from utils4plans.lists import (
    sort_and_group_objects,
    pairwise,
)
from utils4plans.sets import set_difference

from polymap.examples.layout import layout as sample_layout
from polymap.geometry.surfaces import Surface, FancyRange
from polymap.layout.interfaces import create_layout_from_dict
from polymap.layout.interfaces import Layout
from polymap.geometry.vectors import Axes


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
        | where(lambda x: x.domain_name != surf.domain_name)
        | where(lambda x: x.aligned_axis == surf.aligned_axis)
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
        domain_range = closer_domain.get_range_by_axis(closer_surf.direction_axis)

        surf_range = FancyRange(further_surf.location, surf.location)
        if surf_range.contains(domain_range):
            # TODO log
            #     f"`{closer_domain.name}` is contained in the distance betwen the current surf `{surf}` and the further surf on `{further_surf.domain_name}`. Removing the further surf"
            # )
            bad_surfs.append(further_surf)
    remaining = set_difference(other_surfs, bad_surfs)
    return remaining


def get_nbs_for_surf(layout: Layout, surf: Surface):
    potential_nbs = get_candidate_surface_neighbors(layout, surf)
    return filter_candidate_neighbors(layout, surf, potential_nbs)


if __name__ == "__main__":
    layout = create_layout_from_dict(sample_layout)
    surf = layout.get_domain("red").get_surface("south", 1)
    os = get_candidate_surface_neighbors(layout, surf)
    filter_candidate_neighbors(layout, surf, os)
