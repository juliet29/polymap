from utils4plans.lists import get_unique_items_in_list_keep_order
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


@dataclass
class AlphaBend:
    s1: Surface
    s2: Surface
    s3: Surface
    domain: FancyOrthoDomain

    @property
    def get_move(self):
        # TODO: make function that gets the vector component
        return Move(
            self.domain,
            self.s1,
            float(self.s2.vector[1]),  # pyright: ignore[reportArgumentType]
        )


def get_domain(msd_id: MSD_IDs, domain_name: str):
    id, layout = get_one_msd_layout(msd_id)
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


class DefinesMove(Protocol):
    def get_move(self) -> Move: ...


def apply_move(move: Move):
    new_dom = update_domain(*move)
    new_coords = get_unique_items_in_list_keep_order(new_dom.coords)
    return FancyOrthoDomain(new_coords)
