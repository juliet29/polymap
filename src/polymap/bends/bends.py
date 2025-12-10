from itertools import combinations

from utils4plans.lists import get_unique_items_in_list_keep_order
from polymap.bends.interfaces import ZetaBend, PiBend, KappaBend, EtaBend, BendHolder
from utils4plans.sets import set_difference, set_intersection
from polymap.examples.msd import MSD_IDs, get_one_msd_layout
from polymap.geometry.modify.delete import Delete
from polymap.geometry.modify.update import Move, update_domain
from polymap.geometry.ortho import FancyOrthoDomain
from polymap.geometry.surfaces import Surface

from rich import print


TOLERANCE = 0.13  # TODO: make a constant


def get_domain(msd_id: MSD_IDs, domain_name: str):
    _, layout = get_one_msd_layout(msd_id)
    dom = layout.get_domain(domain_name)
    return dom


def find_small_surfs(domain: FancyOrthoDomain, tolerance=TOLERANCE):
    small_surfs = list(filter(lambda x: x.range.size <= tolerance, domain.surfaces))
    return small_surfs


def find_surf_nbs(surfs: list[Surface], target: Surface):
    target_ix = surfs.index(target)
    alpha_ix = (target_ix - 1) % len(surfs)
    beta_ix = (target_ix + 1) % len(surfs)
    alpha, beta = surfs[alpha_ix], surfs[beta_ix]
    return (alpha, target, beta)


def create_zeta_bends(small_surfs: list[Surface], domain: FancyOrthoDomain):
    bends = list(
        map(lambda x: ZetaBend(*find_surf_nbs(domain.surfaces, x), domain), small_surfs)
    )
    return bends


def update_indices(
    found_indices: list[int], bends: list[ZetaBend], b1: ZetaBend, b2: ZetaBend
):
    ix1 = bends.index(b1)
    ix2 = bends.index(b2)
    found_indices.extend([ix1, ix2])
    return found_indices


def get_remain_zetas(found_indices: list[int], bends: list[ZetaBend]):
    remain_indices = set_difference(list(range(len(bends))), found_indices)
    return list(map(lambda x: bends[x], remain_indices))


def handle_pi_bend(b1: ZetaBend, b2: ZetaBend):
    if b1.b == b2.a:
        return PiBend(*b1.surface_tuple, b2.s1, b2.b, b1.domain)
    elif b2.a == b2.b:
        raise NotImplementedError(
            "Zeta bends may be misordered.. add check for sorting.."
        )
    else:
        print("Unexpected pi bend combo!")
        print(b1)
        print(b2)
        raise Exception("Unexpected pi bend combination!")


def handle_kappa_bend(b1: ZetaBend, b2: ZetaBend):
    rel1 = b1.s1 == b2.a
    rel2 = b1.b == b2.s1
    if rel1 and rel2:
        return KappaBend(*b1.surface_tuple, b2.b, b1.domain)
    else:
        raise Exception("Unexpected kappa bend combo")


def handle_eta_bend(b1: ZetaBend, b2: ZetaBend):
    return EtaBend(*b1.surfaces)


def handle_complex_band(
    bh: BendHolder, i: ZetaBend, j: ZetaBend, len_interesection: int
):
    match len_interesection:
        case 1:
            bh.pis.append(handle_pi_bend(i, j))
        case 2:
            bh.kappas.append(handle_kappa_bend(i, j))
        case 3:
            bh.etas.append(handle_eta_bend(i, j))
        case _:
            raise NotImplementedError(
                f"Haven't handled zeta intersection of size {len_interesection}"
            )
    return bh


def check_zeta_intersections(bends: list[ZetaBend]) -> BendHolder:
    if not bends or len(bends) == 1:
        return BendHolder(zetas=bends)

    found_indices: list[int] = []

    combos = combinations(bends, 2)
    bend_holder = BendHolder()
    for i, j in combos:
        intersection = set_intersection(i.surfaces, j.surfaces)

        if intersection:
            found_indices = update_indices(found_indices, bends, i, j)
            bend_holder = handle_complex_band(bend_holder, i, j, len(intersection))

    zetas = get_remain_zetas(found_indices, bends)
    bend_holder.zetas.extend(zetas)
    return bend_holder


MoveDelete = tuple[Move, Delete]


def apply_move(move: Move, delete: Delete | None = None, debug=False):
    new_dom = update_domain(move, delete, debug=debug)
    new_coords = get_unique_items_in_list_keep_order(new_dom.coords)
    return FancyOrthoDomain(new_coords, name=move.domain.name)
