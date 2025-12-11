from typing import NamedTuple

from polymap.bends.bends import get_domain
import shapely as sp
from polymap.bends.iterate import DomainCleanFailureReport, iterate_clean_domain
from polymap.bends.utils import get_msd_domain, make_bend_holder
from polymap.examples.msd import MSD_IDs
from polymap.visuals.visuals import plot_polygon
from rich import print


def plot_coords():

    coords = [
        (-9.502667713879953, 2.61249418007276),
        (-7.591660975523276, 2.61249418007276),
        (-7.591660975523276, 0.7139776818360604),
        # (-7.591660975523276, 0.7139776818360604),
        # (-7.591660975523276, 0.7389581620760168),
        (-6.644402726404927, 0.7389581620760168),
        (-6.644402726404927, -1.1075973756807675),
        (-9.502667713879953, -1.1075973756807675),
    ]
    poly = sp.Polygon(coords)
    plot_polygon(poly, show=True)


def test_fix_kappa():
    domain_name = "kitchen_3"
    id: MSD_IDs = "58613"
    dom = get_domain(id, domain_name)
    bh = make_bend_holder(dom)
    k = bh.kappas[0]  # TODO: add a next method
    print(str(k))
    # new_dom = apply_move(k.get_move[0])
    # plot_domain_move(dom, new_dom, k.surfaces)
    #


all_bad_doms2 = [
    # pi bends at the end of the vector list
    "106493-kitchen_7",  # invalid pi bend
    "27540-shaft_10",  # bad pi bend? -> reverse..
]

gammas = [
    # kappa that is gamma
    # "146915-living_room_8", # kappa that is gamma
    "27540-kitchen_9",  # kappa that is really gamma
    # "27540-living_dining_4", # kappa that is gamma
    "48205-room_9",  # kappa that is gamma
]

inner_bend_kappas = [
    # kappas that are inner bends...
    "146915-kitchen_5",  # bad kappa
    "146965-kitchen_5",  # bad kappa
    "49943-bathroom_0",  # inner kappa / bad kappa
    "49943-room_18",  # inner kappa
    "49943-room_4",  # inner kappa
]

zero_vectors = [
    # vectors not getting cleaned up
    "146915-room_6",  # pi-bend, zero vector not cleaned up..
    "71308-kitchen_0",  # zeta, zero vector not cleaned up..
    "71318-kitchen_5",  # zeta, zero vector not cleaned up
]


new_issues = ["48204-room_0", "48205-corridor_2"]


class Failures(NamedTuple):
    name: str
    reason: str


def summarize_failures(fails: list[Failures]):
    print(f"[bold]\nSummarizing run - {len(fails)} failures:")
    print([f.name for f in fails])
    print("geom fails")
    print([f.name for f in fails if "Move" in f.reason])
    for f in fails:
        print(f)


def test_fix_bad_domains():
    fails: list[Failures] = []

    def test(name):

        dname, dom = get_msd_domain(name)
        res = iterate_clean_domain(
            dom, dname.msd_id, show_complete_iteration=False, show_failure=True
        )

    for name in all_bad_doms2:
        print(f"[bold italic yellow]\n{name}")
        try:
            test(name)
        except DomainCleanFailureReport as e:
            fails.append(Failures(name, str(e)))
            print(f"[bold italic magenta]{name} failed in outer loop")

    summarize_failures(fails)


def test_bends_one():
    domain_name = "shaft_10"
    id: MSD_IDs = "27540"
    dom = get_domain(id, domain_name)
    bh = make_bend_holder(dom)
    iterate_clean_domain(dom, id, show_failure=True)
    # apply_move(bh.betas[0].get_move)


if __name__ == "__main__":
    # test_bends_one()
    test_fix_bad_domains()
