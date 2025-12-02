from itertools import combinations
from utils4plans.sets import set_difference, set_intersection
from utils4plans.lists import get_unique_items_in_list_keep_order
import geom
from polymap.examples.msd import MSD_IDs, get_one_msd_layout
from polymap.geometry.ortho import FancyOrthoDomain
from polymap.geometry.surfaces import Surface
from dataclasses import dataclass
from typing import NamedTuple, Protocol

from polymap.geometry.update import update_domain

TOLERANCE = 0.13  # TODO: make a constant


class Move(NamedTuple):
    domain: FancyOrthoDomain
    surface: Surface
    delta: float


class DefinesMove(Protocol):
    def get_move(self) -> Move: ...


def get_component(v: geom.Vector, ix: int):
    return float(v[ix])  # pyright: ignore[reportArgumentType]


@dataclass
class ZetaBend:
    s1: Surface
    s2: Surface
    s3: Surface
    domain: FancyOrthoDomain

    @property
    def surfaces(self):
        return [self.s1, self.s2, self.s3]

    @property
    def surface_tuple(self):
        return (self.s1, self.s2, self.s3)

    @property
    def get_move(self):
        return Move(
            self.domain, self.s1, get_component(self.s2.vector, 1)
        )  # TODO: this should really be get value, for the case of vertical bend..


@dataclass
class PiBend:
    s1: Surface
    s2: Surface
    s3: Surface
    s4: Surface
    s5: Surface
    domain: FancyOrthoDomain

    @property
    def surfaces(self):
        return [self.s1, self.s2, self.s3, self.s4, self.s5]

    @property
    def get_move(self):
        return Move(self.domain, self.s3, get_component(self.s2.vector, 1))


def get_domain(msd_id: MSD_IDs, domain_name: str):
    _, layout = get_one_msd_layout(msd_id)
    dom = layout.get_domain(domain_name)
    return dom


def find_small_surfs(domain: FancyOrthoDomain, tolerance=0.13):
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
    if b1.s3 == b2.s1:
        return PiBend(*b1.surface_tuple, b2.s2, b2.s3, b1.domain)
    elif b2.s1 == b2.s3:
        raise NotImplementedError(
            "Zeta bends may be misordered.. add check for sorting.."
        )
    else:
        raise Exception("Unexpected pi bend combination!")


def check_zeta_intersections(bends: list[ZetaBend]):
    if not bends or len(bends) == 1:
        return bends, []

    found_indices: list[int] = []
    pis: list[PiBend] = []
    combos = combinations(bends, 2)

    for i, j in combos:
        intersection = set_intersection(i.surfaces, j.surfaces)

        if intersection:
            found_indices = update_indices(found_indices, bends, i, j)

            if len(intersection) > 1:
                raise NotImplementedError("Haven't handled more complex bends")

            pi_bend = handle_pi_bend(i, j)
            pis.append(pi_bend)
            # print(intersection)

    zetas = get_remain_zetas(found_indices, bends)
    return zetas, pis


def apply_move(move: Move):
    new_dom = update_domain(*move)
    new_coords = get_unique_items_in_list_keep_order(new_dom.coords)
    return FancyOrthoDomain(new_coords)
