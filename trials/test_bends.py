from rich import print
from polymap.bends.bends import (
    apply_move,
    check_zeta_intersections,
    create_zeta_bends,
    find_small_surfs,
    get_domain,
)
from polymap.bends.iterate import iterate_clean_domain
from polymap.bends.points import heal_extra_points_on_domain
from polymap.bends.viz import plot_domain_move
from polymap.examples.msd import MSD_IDs, get_one_msd_layout
from polymap.geometry.ortho import FancyOrthoDomain


def handle_domain(dom: FancyOrthoDomain, id: MSD_IDs):
    surfs = find_small_surfs(dom)
    zeta_bends = create_zeta_bends(surfs, dom)
    pis = []
    zetas = []

    try:
        zetas, pis = check_zeta_intersections(zeta_bends)
    except NotImplementedError as e:
        print(e)
        return

    if pis:
        print(pis)
        dom2 = apply_move(pis[0].get_move)
        dom3 = heal_extra_points_on_domain(dom2)
        plot_domain_move(dom, dom3, pis[0].surfaces, id=id)

    if zetas:
        print(zetas)
        dom2 = apply_move(zetas[0].get_move)
        dom3 = heal_extra_points_on_domain(dom2)
        plot_domain_move(dom, dom3, zetas[0].surfaces, id=id)


def test_bends():
    id: MSD_IDs = "67372"
    _, layout = get_one_msd_layout(id)
    domains = layout.domains
    for dom in domains:
        print(f"\n{dom.name.upper()=}")
        try:
            iterate_clean_domain(dom, id)
        except NotImplementedError as e:
            print(e)
            continue


def test_bends_one():
    domain_name = "balcony_0"
    id: MSD_IDs = "106493"
    dom = get_domain(id, domain_name)
    iterate_clean_domain(dom, id)


if __name__ == "__main__":
    test_bends()
