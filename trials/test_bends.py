from rich import print
from polymap.bends.bends import (
    apply_move,
    check_zeta_intersections,
    create_zeta_bends,
    find_small_surfs,
)
from polymap.bends.viz import plot_domain_move
from polymap.examples.msd import MSD_IDs, get_one_msd_layout


def test_bends():
    domain_name = "balcony_0"
    id: MSD_IDs = "67372"
    # dom = get_domain(id, domain_name)
    _, layout = get_one_msd_layout(id)
    domains = layout.domains
    for dom in domains:
        print(f"\n{dom.name=}")

        surfs = find_small_surfs(dom)

        if not surfs:
            print(f"No small surfs for {dom.name}")
            continue
        zeta_bends = create_zeta_bends(surfs, dom)
        pis = []
        zetas = []

        try:
            zetas, pis = check_zeta_intersections(zeta_bends)
        except NotImplementedError as e:
            print(e)
            continue

        if pis:
            print(pis)
            dom2 = apply_move(pis[0].get_move)
            plot_domain_move(dom, dom2, pis[0].surfaces, id=id)

        if zetas:
            print(zetas)
            dom2 = apply_move(zetas[0].get_move)
            plot_domain_move(dom, dom2, zetas[0].surfaces, id=id)


if __name__ == "__main__":
    test_bends()
