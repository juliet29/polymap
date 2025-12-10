from polymap.bends.bends import (
    get_domain,
)
from polymap.bends.utils import make_bend_holder
from polymap.examples.msd import MSD_IDs
from polymap.visuals.visuals import plot_polygon


def test_identify_zeta():
    domain_name = "balcony_0"
    id: MSD_IDs = "67372"
    dom = get_domain(id, domain_name)
    bh = make_bend_holder(dom)
    assert len(bh.zetas) == 1


def test_identify_beta():
    domain_name = "kitchen_9"
    id: MSD_IDs = "27540"
    dom = get_domain(id, domain_name)
    bh = make_bend_holder(dom)
    assert len(bh.betas) == 1


def test_identify_pi():
    domain_name = "balcony_0"
    id: MSD_IDs = "106493"
    dom = get_domain(id, domain_name)
    bh = make_bend_holder(dom)
    assert len(bh.pis) == 2


def test_identify_kappa():
    domain_name = "kitchen_3"
    id: MSD_IDs = "58613"
    dom = get_domain(id, domain_name)
    bh = make_bend_holder(dom)
    assert len(bh.kappas) == 1


def test_identify_gamma():
    domain_name = "room_9"
    id: MSD_IDs = "48205"
    dom = get_domain(id, domain_name)
    plot_polygon(dom.polygon, show=True)
    dom.summarize_surfaces()
    bh = make_bend_holder(dom)
    assert len(bh.gammas) == 1
    #


# TODO : this is a trial thing
def see_bh_general(domain_name: str, id: MSD_IDs):
    dom = get_domain(id, domain_name)
    dom.summarize_surfaces()
    make_bend_holder(dom)
    plot_polygon(dom.polygon, show=True)


if __name__ == "__main__":
    test_identify_beta()
