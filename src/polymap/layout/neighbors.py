from pipe import where

from utils4plans.lists import sort_and_group_objects
from utils4plans.sets import set_difference

from polymap.examples.layout import layout as sample_layout
from polymap.geometry.surfaces import Surface, FancyRange
from polymap.geometry.ortho import FancyOrthoDomain
from polymap.layout.interfaces import create_layout_from_dict
from polymap.layout.interfaces import Layout
from rich import print


def get_candidate_surface_neighbors(layout: Layout, surf: Surface):
    # SPlit into three functions and move elsewhere -> no longer just geometry
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

    print(f"curr_surf={surf.name}, loc={surf.location:.2f}")
    print([(i.name, f"{i.location:.2f}") for i in res])

    return best_surface_for_each_domain(res)


def sort_surfaces(surf: Surface, other_surfs: list[Surface]):
    sorted_surfs = sorted(other_surfs, key=lambda x: x.location, reverse=True)
    furthest, closest = sorted_surfs[0], sorted_surfs[-1]
    max_range = FancyRange(surf.location, furthest.location)
    min_range = FancyRange(surf.location, closest.location)
    assert max_range.size >= min_range.size
    return sorted_surfs


def make_virtual_domain(
    surf: Surface,
    further_surf: Surface,
):
    distance_range = FancyRange(surf.location, further_surf.location)
    axis_aligned_range = surf.range.intersection(further_surf.range, surf.parallel_axis)
    print(f"{axis_aligned_range=}")

    if surf.parallel_axis == "X":
        virtual_domain = FancyOrthoDomain.from_bounds(
            *axis_aligned_range.as_tuple, *distance_range.as_tuple
        )
    else:
        virtual_domain = FancyOrthoDomain.from_bounds(
            *distance_range.as_tuple, *axis_aligned_range.as_tuple
        )
    return virtual_domain


def is_bad_surf(
    layout: Layout,
    other_surfs: list[Surface],
    virtual_domain: FancyOrthoDomain,
    further_surf_ix: int,
):
    # NOTE: cant be a bad surf bc it is the closest, by virtue of being at the end of the list
    if further_surf_ix + 1 == len(other_surfs):
        return False
    for surf in other_surfs[further_surf_ix + 1 :]:
        closer_poly = layout.get_domain(surf.domain_name).polygon
        virtual_poly = virtual_domain.polygon
        if virtual_poly.intersects(closer_poly):
            fs = other_surfs[further_surf_ix]
            print(
                f"{fs.name}'s virtual domain intersects {surf.domain_name}. Eliminating {fs.name}..."
            )
            return True


def filter_candidate_neighbors(
    layout: Layout, surf: Surface, other_surfs: list[Surface]
):
    # NOTE: neighbor furthest away from the current surf is first
    sorted_surfs = sort_surfaces(surf, other_surfs)
    print("\nsorted_surfs=")
    print(sorted_surfs)
    bad_surfs = []

    for further_surf in sorted_surfs:
        further_surf_ix = sorted_surfs.index(further_surf)
        print(f"{further_surf_ix=}")
        # closer_domain = layout.get_domain(closer_surf.domain_name)

        virtual_domain = make_virtual_domain(surf, further_surf)

        if is_bad_surf(layout, other_surfs, virtual_domain, further_surf_ix):
            bad_surfs.append(further_surf)

    remaining = set_difference(other_surfs, bad_surfs)
    print("\nremaining=")
    print(remaining)

    # print(f"{str(surf)}: {[i.domain_name for i in bad_surfs]}")
    return remaining


def get_nbs_for_surf(layout: Layout, surf: Surface):
    potential_nbs = get_candidate_surface_neighbors(layout, surf)
    # return potential_nbs
    print("\npotential_nbs=")
    print(potential_nbs)
    if not potential_nbs:
        return []
    return filter_candidate_neighbors(layout, surf, potential_nbs)


if __name__ == "__main__":
    layout = create_layout_from_dict(sample_layout)
    surf = layout.get_domain("red").get_surface("south", 1)
    os = get_candidate_surface_neighbors(layout, surf)
    # filter_candidate_neighbors(layout, surf, os)
