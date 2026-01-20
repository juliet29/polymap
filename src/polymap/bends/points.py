from typing import Any, NamedTuple
from loguru import logger
import shapely as sp
from utils4plans.geom import tuple_list_from_list_of_coords
from polymap.geometry.modify.validate import validate_polygon
from polymap.geometry.ortho import FancyOrthoDomain
from itertools import groupby

from polymap.geometry.surfaces import Surface, create_surface
from polymap.geometry.vectors import vector_from_coords
from polymap.geometry.paired_coords import PairedCoord, coords_from_paired_coords_list
from rich import print


DEBUG = False


class GroupByResult(NamedTuple):
    group_name: Any
    items: list[Any]

    # @property
    # def items(self):
    #     return list(self.group_list)


def find_vector_groups_on_domain(domain: FancyOrthoDomain, debug=DEBUG):
    gres = groupby(domain.surfaces, key=lambda x: x.rounded_norm_vector)
    result = [GroupByResult(i[0], list(i[1])) for i in gres]

    if debug:
        print("VECTOR GROUPS=")
        for group_name, items in result:
            print(f"{group_name}: {[i.name for i in items]}")
    # TODO: add to utils4plans, group objects without sorting...
    groups = list(map(lambda x: list(x[1]), result))

    return groups


# second type of vector group => vectors that are separated only by small surface..


def find_new_surf_for_vector_group(surfs: list[Surface], domain_name: str):
    # TODO: assert that the surfaces are sorted!
    c0 = surfs[0].coords.first
    c1 = surfs[-1].coords.last
    new_paired_coords = PairedCoord(c0, c1)
    new_v = vector_from_coords(c0, c1)
    new_surf = create_surface(new_v, new_paired_coords, domain_name)

    # NOTE: the index of this surface only becomes valid after it is added to a domain!
    return new_surf


def fix_vector_group_on_domain(domain: FancyOrthoDomain, surfs: list[Surface]):
    logger.debug(f"surf group to heal: {[i.name_w_domain for i in surfs]}")
    new_surf = find_new_surf_for_vector_group(surfs, domain.name)
    surf_indices = [domain.surfaces.index(i) for i in surfs]
    min_ix, max_ix = surf_indices[0], surf_indices[-1]

    def get_surfs(start_ix: int, end_ix: int):
        res = [domain.surfaces[ix] for ix in range(start_ix, end_ix)]
        return res

    len_surfs = len(domain.surfaces)

    new_surfs = get_surfs(0, min_ix) + [new_surf] + get_surfs(max_ix + 1, len_surfs)

    new_coords = coords_from_paired_coords_list([i.coords for i in new_surfs])

    test_poly = sp.Polygon(tuple_list_from_list_of_coords(new_coords))
    validate_polygon(test_poly, domain.name)

    dom = FancyOrthoDomain(new_coords, domain.name)
    return dom


def heal_extra_points_on_domain(domain: FancyOrthoDomain):
    vector_groups = find_vector_groups_on_domain(domain)
    problem_groups = list(filter(lambda x: len(x) > 1, vector_groups))

    if len(problem_groups) == 0:
        return domain

    if len(problem_groups) > 1:
        raise Exception("Should only have one problem group at a time!")

    return fix_vector_group_on_domain(domain, problem_groups[0])
