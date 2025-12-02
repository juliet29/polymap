from rich import print
from polymap.bends.bends import (
    check_zeta_intersections,
    create_zeta_bends,
    find_small_surfs,
    get_domain,
)


def test_bends():
    domain_name = "balcony_0"
    id = "106493"
    dom = get_domain(id, domain_name)

    surfs = find_small_surfs(dom)
    zeta_bends = create_zeta_bends(surfs, dom)
    zetas, pis = check_zeta_intersections(zeta_bends)
    print(zetas)
    print(pis)

    # count = 0
    # while surfs:
    #     nbs = find_surf_nbs(dom.surfaces, surfs[0])
    #
    #     ab = ZetaBend(*nbs, dom)
    #     dom2 = apply_move(ab.get_move)
    #     plot_domain_move(dom, dom2, list(nbs), id=id)
    #     print(surfs)
    #
    #     dom = dom2
    #     surfs = find_small_surfs(dom)
    #
    #     if not surfs:
    #         break
    #     count += 1
    #     if count > 5:
    #         break
    #
    # plot_domain_and_surf(dom, list(nbs), title=title)

    # domain2 = update_domain(*move)
    # print([(i, i.mag()) for i in domain2.vectors])
    #
    # print(list(map(lambda x: str(x), domain2.coords)))
    #
    # new_coords = get_unique_items_in_list_keep_order(domain2.coords)
    # print(list(map(lambda x: str(x), new_coords)))

    # plot_domain_move(dom, domain2, list(nbs), id=id)

    # ix = dom.surfaces.index(nbs[1])
    #
    # vix = dom.vectors[ix]
    # print(vix)
    #
    # print(nbs)


if __name__ == "__main__":
    test_bends()
