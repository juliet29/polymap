from copy import deepcopy
from typing import NamedTuple
from pipe import where

from utils4plans.lists import chain_flatten, sort_and_group_objects

from polymap.examples.layout import layout_coords as sample_layout
from polymap.geometry.surfaces import Surface, FancyRange
from polymap.geometry.ortho import FancyOrthoDomain
from polymap.geometry.layout import create_layout_from_dict
from polymap.geometry.layout import Layout


def get_candidate_surface_neighbors(layout: Layout, surf: Surface):
    def best_surface_for_each_domain(surfs: list[Surface]):
        best_surfs = []
        res = sort_and_group_objects(surfs, lambda x: x.domain_name)
        for group in res:
            sort_surfs = sorted(group, key=lambda x: x.location, reverse=False)
            best_surfs.append(sort_surfs[0])

        return best_surfs

    res = list(
        layout.get_other_surfaces(surf, substantial_only=True)
        | where(lambda x: x.domain_name != surf.domain_name)
        | where(lambda x: x.parallel_axis == surf.parallel_axis)
        | where(lambda x: surf.range.is_coincident(x.range))
        | where(lambda x: x.location >= surf.location)
    )

    return best_surface_for_each_domain(res)


def sort_surfaces(surf: Surface, other_surfs: list[Surface]):
    sorted_surfs = sorted(other_surfs, key=lambda x: x.location, reverse=True)
    furthest, closest = sorted_surfs[0], sorted_surfs[-1]
    max_range = FancyRange(surf.location, furthest.location)
    min_range = FancyRange(surf.location, closest.location)
    assert max_range.size >= min_range.size
    # logger.info(
    #     f"curr_surf: {(surf.name_w_domain, surf.location)} \nsorted surfaces: {[(i.name_w_domain, i.location) for i in sorted_surfs]} "
    # )
    return sorted_surfs


def make_virtual_domain(
    surf: Surface,
    further_surf: Surface,
):
    distance_range = FancyRange(surf.location, further_surf.location)
    axis_aligned_range = surf.range.intersection(further_surf.range, surf.parallel_axis)

    if surf.parallel_axis == "X":
        virtual_domain = FancyOrthoDomain.from_bounds(
            *axis_aligned_range.as_tuple, *distance_range.as_tuple
        )
    else:
        virtual_domain = FancyOrthoDomain.from_bounds(
            *distance_range.as_tuple, *axis_aligned_range.as_tuple
        )
    return virtual_domain


class CompPair(NamedTuple):
    further: Surface
    closer: Surface


def generate_neigbor_comparisons(other_surfs: list[Surface]):
    def gen(item: Surface):
        ix = other_surfs.index(item)
        remain_list = other_surfs[ix + 1 :]
        pairs = [CompPair(item, i) for i in remain_list]
        return pairs

    assert other_surfs[0].location >= other_surfs[1].location
    res = [gen(i) for i in other_surfs]
    return chain_flatten(res)


def filter_neigbors(
    layout: Layout,
    surface: Surface,
    potential_nbs: list[Surface],
    comparisons: list[CompPair],
):
    potential_nbs_local = deepcopy(potential_nbs)

    for pair in comparisons:
        if pair.further in potential_nbs_local:
            far_poly = make_virtual_domain(surface, pair.further).polygon
            close_poly = layout.get_domain(pair.closer.domain_name).polygon
            res = far_poly.intersects(close_poly)
            if res:
                potential_nbs_local.remove(pair.further)

    # logger.info(
    #     f"remaining potential_nbs: {[i.name_w_domain for i in potential_nbs_local]}"
    # )

    return potential_nbs_local


def get_nbs_for_surf(layout: Layout, surf: Surface):

    potential_nbs = get_candidate_surface_neighbors(layout, surf)
    if not potential_nbs:
        # logger.log("END", f"No potential nbs for {surf.name_w_domain}. Exiting ...")
        #
        return []

    # logger.log("START", f"############ {surf.name_w_domain} ################")

    if len(potential_nbs) > 1:

        sorted_potential_nbs = sort_surfaces(surf, potential_nbs)
        comparisons = generate_neigbor_comparisons(sorted_potential_nbs)
        true_nbs = filter_neigbors(layout, surf, sorted_potential_nbs, comparisons)

    else:
        true_nbs = potential_nbs

    summary = {
        "Surface": surf.name_w_domain,
        "Potential": [i.name_w_domain for i in potential_nbs],
        "True": [i.name_w_domain for i in true_nbs],
    }

    # logger.log("SUMMARY", pretty_repr(summary))
    return true_nbs


if __name__ == "__main__":
    layout = create_layout_from_dict(sample_layout)
    surf = layout.get_domain("red").get_surface("south", 1)
    os = get_candidate_surface_neighbors(layout, surf)
    # filter_candidate_neighbors(layout, surf, os)
