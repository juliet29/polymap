from copy import deepcopy
from dataclasses import dataclass
from typing import Literal
from utils4plans.lists import get_unique_items_in_list_keep_order
from utils4plans.sets import set_difference
from polymap.geometry.modify.update import Move, update_domain
from polymap.geometry.ortho import FancyOrthoDomain
from polymap.geometry.shapely_helpers import get_coords_from_shapely_geom
import shapely as sp
from polymap.geometry.surfaces import Surface
from polymap.interfaces import PairedCoord
from polymap.geometry.vectors import Axes
from rich import print


def segment_coords_center(
    coords: PairedCoord,
    axis: Axes,
    length: float,
):
    line = coords.shapely_line
    center = line.centroid

    if axis == "X":
        translation = (length, 0)
    else:
        translation = (0, length)

    new_coord = sp.affinity.translate(center, *translation)
    b1 = get_coords_from_shapely_geom(center)[0]
    b2 = get_coords_from_shapely_geom(new_coord)[0]

    return (coords.first, b1, b2, coords.last)


def segment_coords_end(coords: PairedCoord, axis: Axes, length: float):
    end = sp.Point(coords.last.as_tuple)

    if axis == "X":
        translation = (-length, 0)
    else:
        translation = (0, -length)

    new_point = sp.affinity.translate(end, *translation)

    new_coord = get_coords_from_shapely_geom(new_point)[0]

    return (coords.first, new_coord, coords.last)


def segment_surface_and_update_domain(
    domain: FancyOrthoDomain,
    surf: Surface,
    length: float,
    segment_type: Literal["center", "end"],
):

    if segment_type == "center":
        new_surf_coords = segment_coords_center(surf.coords, surf.parallel_axis, length)
    else:
        new_surf_coords = segment_coords_end(surf.coords, surf.parallel_axis, length)
    curr_coords = deepcopy(domain.normalized_coords)

    first_ix = curr_coords.index(new_surf_coords[0])
    for ix, coord in enumerate(new_surf_coords):
        curr_coords.insert(first_ix + ix, coord)

    res = get_unique_items_in_list_keep_order(curr_coords)
    return FancyOrthoDomain(res, domain.name)


@dataclass
class BendyDomainCreator:
    domain: FancyOrthoDomain
    surface: Surface
    length: float = 0.10

    def kappa_one(self):
        surf_len = self.surface.range.size

        seg = segment_surface_and_update_domain(
            self.domain, self.surface, surf_len / 2, "end"
        )
        self.domain.summarize_surfaces()
        seg.summarize_surfaces()
        new_surfs = sorted(
            set_difference(seg.surfaces, self.domain.surfaces),
            key=lambda x: x.direction_ix,
        )
        new_surf = new_surfs[-1]
        print(new_surfs)
        print(new_surf)
        # small_surf = find_small_surfs(seg)[0]
        # # actually want the one after..
        # bn = BendNeighbors(*find_surf_nbs(seg.surfaces, new_surf))
        m = Move(seg, new_surf, -self.length)

        result = update_domain(m)
        return result
