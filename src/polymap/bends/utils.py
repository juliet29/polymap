from typing import NamedTuple, get_args
from polymap.bends.bends import (
    check_eta_intersections,
    create_eta_bends,
    find_small_surfs,
    get_domain,
)
from polymap.examples.msd import MSD_IDs
from polymap.geometry.ortho import FancyOrthoDomain


def make_bend_holder(dom: FancyOrthoDomain):
    surfs = find_small_surfs(dom)
    zeta_bends = create_eta_bends(surfs, dom)
    bend_holder = check_eta_intersections(zeta_bends)
    bend_holder.summarize()

    return bend_holder


class DomainName(NamedTuple):
    id: str
    room_type: str
    ix: str

    @property
    def msd_id(self) -> MSD_IDs:
        assert self.id in get_args(MSD_IDs)
        id: MSD_IDs = self.id  # pyright: ignore[reportAssignmentType]
        return id

    @property
    def domain_name(self):
        return f"{self.room_type}_{self.ix}"


def get_msd_domain(name: str):
    dname = DomainName(*name.split("_"))
    dom = get_domain(dname.msd_id, dname.domain_name)
    return dname, dom
