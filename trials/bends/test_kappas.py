from typing import NamedTuple
from polymap.bends.bends import find_small_surfs, get_domain
import shapely as sp
from polymap.bends.iterate import determine_bend_to_fix, iterate_clean_domain
from polymap.bends.utils import get_msd_domain, make_bend_holder
from polymap.examples.msd import MSD_IDs
from polymap.geometry.modify.update import update_domain
from polymap.visuals.visuals import plot_polygon
from rich import print


def test_bends_one():
    domain_name = "kitchen_3"
    id: MSD_IDs = "58613"
    dom = get_domain(id, domain_name)
    surfs = find_small_surfs(dom)
    bends_to_fix = determine_bend_to_fix(surfs, dom)
    update_domain(bends_to_fix.get_move)


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


BAD_DOMAINS = [
    "106493_kitchen_7",
    "22940_corridor_6",
    "27540_corridor_1",
    "27540_kitchen_9",
    "27540_shaft_10",
    "49943_room_8",
    "49943_room_14",
    "49943_room_18",
    "49943_corridor_21",
    "58613_kitchen_3",
    "60532_corridor_5",
]
geom_fails = [
    "27540_kitchen_9",
    "49943_room_8",
    "49943_room_14",
    "49943_room_18",
    "49943_corridor_21",
    "60532_corridor_5",
]


class Failures(NamedTuple):
    name: str
    reason: str


def summarize_failures(fails: list[Failures]):
    print([f.name for f in fails])
    print("geom fails")
    print([f.name for f in fails if "POLYGON" in f.reason])
    for f in fails:
        print(f)


def test_fix_bad_domains():
    fails: list[Failures] = []

    def test(name):

        dname, dom = get_msd_domain(name)
        res = iterate_clean_domain(dom, dname.msd_id, debug=True)

    for name in geom_fails:
        print(f"[bold italic yellow]\n{name}")
        try:
            test(name)
        except Exception as e:
            fails.append(Failures(name, str(e)))
            print(f"[bold italic magenta]{name} failed in outer loop")

    summarize_failures(fails)


if __name__ == "__main__":
    # test_bends_one()
    test_fix_bad_domains()
