from itertools import combinations

from utils4plans.lists import get_unique_items_in_list_keep_order
from polymap.bends.interfaces import (
    EtaBend,
    PiBend,
    KappaBend,
    GammaBend,
    BendHolder,
    ZetaBend,
    BetaBend,
    Bend,
    ProblemIdentifyingBend,
)
from utils4plans.sets import set_difference, set_intersection
from polymap.examples.msd import MSD_IDs, get_one_msd_layout
from polymap.geometry.modify.delete import Delete
from polymap.geometry.modify.update import Move, update_domain
from polymap.geometry.ortho import FancyOrthoDomain
from polymap.geometry.surfaces import Surface
from rich import print


TOLERANCE = 0.13  # TODO: make a constant


def show_problem_bends(bends: list[Bend]):
    print("[bold blue]Problem Bends:")
    for b in bends:
        print(str(b))


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


def create_eta_bends(small_surfs: list[Surface], domain: FancyOrthoDomain):
    bends = list(
        map(lambda x: EtaBend(*find_surf_nbs(domain.surfaces, x), domain), small_surfs)
    )
    return bends


def update_indices(
    found_indices: list[int], bends: list[EtaBend], b1: EtaBend, b2: EtaBend
):
    ix1 = bends.index(b1)
    ix2 = bends.index(b2)
    found_indices.extend([ix1, ix2])
    return found_indices


def get_remain_etas(found_indices: list[int], bends: list[EtaBend]):
    remain_indices = set_difference(list(range(len(bends))), found_indices)
    return list(map(lambda x: bends[x], remain_indices))


def handle_pi_bend(b1: EtaBend, b2: EtaBend):
    if b1.b == b2.a:
        return PiBend(*b1.surface_tuple, b2.s1, b2.b, b1.domain)
    elif b2.a == b2.b:
        raise ProblemIdentifyingBend(
            "Zeta bends may be misordered.. add check for sorting..", [b1, b2]
        )
    else:
        raise ProblemIdentifyingBend("Unexpected pi bend combination!", [b1, b2])


def handle_kappa_bend(b1: EtaBend, b2: EtaBend):
    rel1 = b1.s1 == b2.a
    rel2 = b1.b == b2.s1
    if rel1 and rel2:
        return KappaBend(*b1.surface_tuple, b2.b, b1.domain)
    else:
        raise ProblemIdentifyingBend("Unexpected kappa bend combo", [b1, b2])


def handle_gamma_bend(b1: EtaBend, b2: EtaBend):
    return GammaBend(*b1.surfaces)


def handle_complex_bend(bh: BendHolder, i: EtaBend, j: EtaBend, len_interesection: int):
    match len_interesection:
        case 1:
            bh.pis.append(handle_pi_bend(i, j))
        case 2:
            bh.kappas.append(handle_kappa_bend(i, j))
        case 3:
            bh.gammas.append(handle_gamma_bend(i, j))
        case _:
            raise ProblemIdentifyingBend(
                f"Haven't handled zeta intersection of size {len_interesection}", [i, j]
            )
    return bh


def distinguish_eta_bends(bend_holder: BendHolder):

    def distinguish(eta: EtaBend):
        zeta_cond = eta.a.direction == eta.b.direction
        beta_cond = (
            eta.a.direction.aligned_vector == -1 * eta.b.direction.aligned_vector
        )
        if zeta_cond:
            bend_holder.zetas.append(ZetaBend.from_eta(eta))
        elif beta_cond:
            bend_holder.betas.append(BetaBend.from_eta(eta))
        else:
            raise ProblemIdentifyingBend("Invalid ZetaBend!", [eta])
        return bend_holder

    for eta in bend_holder.etas:
        bend_holder = distinguish(eta)

    return bend_holder


def check_eta_intersections(bends: list[EtaBend]) -> BendHolder:
    if not bends or len(bends) == 1:

        bend_holder = distinguish_eta_bends(BendHolder(etas=bends))

        return bend_holder

    found_indices: list[int] = []

    combos = combinations(bends, 2)
    bend_holder = BendHolder()
    for i, j in combos:
        intersection = set_intersection(i.surfaces, j.surfaces)

        if intersection:
            found_indices = update_indices(found_indices, bends, i, j)
            bend_holder = handle_complex_bend(bend_holder, i, j, len(intersection))

    etas = get_remain_etas(found_indices, bends)
    bend_holder.etas.extend(etas)
    bend_holder = distinguish_eta_bends(bend_holder)
    return bend_holder


# TODO go back to how was before!
# def apply_move(moves: list[Move], debug=False):
#     if len(moves) == 1:
#         move = moves[0]
#         move2 = None
#     elif len(moves) == 2:
#         move, move2 = moves
#     else:
#         raise Exception("Bad moves")
#     try:
#         new_dom = update_domain(move, debug=debug)
#     except InvalidPolygonError as e:
#         if move2:
#             try:
#                 new_dom = update_domain(move2, debug=debug)
#             except InvalidPolygonError as e:
#                 raise InvalidPolygonError(move.domain.polygon, str(e), move.domain.name)
#
#         else:
#             raise InvalidPolygonError(move.domain.polygon, str(e), move.domain.name)
def apply_move(
    moves: list[Move], delete: Delete | None = None, show_failing_polygon=False
):
    move = moves[0]
    new_dom = update_domain(move, delete, show_failing_polygon=show_failing_polygon)
    new_coords = get_unique_items_in_list_keep_order(new_dom.coords)
    return FancyOrthoDomain(new_coords, name=move.domain.name)
