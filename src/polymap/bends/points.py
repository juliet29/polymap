from polymap.geometry.ortho import FancyOrthoDomain
from itertools import groupby

from polymap.geometry.surfaces import Surface, create_surface
from polymap.geometry.vectors import vector_from_coords
from polymap.interfaces import PairedCoord, coords_from_paired_coords_list


def find_vector_groups_on_domain(domain: FancyOrthoDomain):
    result = groupby(domain.surfaces, key=lambda x: x.vector.norm())
    # TODO: add to utils4plans, group objects without sorting...
    groups = list(map(lambda x: list(x[1]), result))
    return groups


def find_new_surf_for_vector_group(surfs: list[Surface], domain_name: str):
    # TODO: assert that the surfaces are sorted!
    c0 = surfs[0].coords.first
    c1 = surfs[-1].coords.last
    new_paired_coords = PairedCoord(c0, c1)
    new_v = vector_from_coords(c0, c1)
    new_surf = create_surface(new_v, new_paired_coords, domain_name)

    # NOTE: the index of this surface only becomes valid after it is added to a domain!
    return new_surf


def remove_extra_points_from_domain(domain: FancyOrthoDomain, surfs: list[Surface]):
    surf_indices = [domain.surfaces.index(i) for i in surfs]
    min_ix, max_ix = surf_indices[0], surf_indices[-1]
    new_surf = find_new_surf_for_vector_group(surfs, domain.name)

    def get_surfs(start_ix: int, end_ix: int):
        res = [domain.surfaces[ix] for ix in range(start_ix, end_ix)]
        # print([i.name for i in res])

        return res

    len_surfs = len(domain.surfaces)

    new_surfs = get_surfs(0, min_ix) + [new_surf] + get_surfs(max_ix + 1, len_surfs)

    # for n in new_surfs:
    #     print(n.name)

    new_coords = coords_from_paired_coords_list([i.coords for i in new_surfs])
    return FancyOrthoDomain(new_coords, domain.name)
