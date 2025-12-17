from polymap.bends.generate import BendyDomainCreator, segment_surface_and_update_domain
from polymap.examples.sample_domains import create_ortho_domain
from polymap.geometry.modify.validate import InvalidPolygonError
from rich import print


def test_segment_surf_and_update_domain_center():
    dom = create_ortho_domain("SQUARE")
    surf = dom.get_surface("north")
    res = segment_surface_and_update_domain(dom, surf, 0.01, "center")
    assert len(res.surfaces) == len(dom.surfaces) + 2


def test_segment_surf_and_update_domain_end():
    dom = create_ortho_domain("SQUARE")
    surf = dom.get_surface("west")
    res = segment_surface_and_update_domain(dom, surf, 0.01, "end")

    assert len(res.surfaces) == len(dom.surfaces) + 1


def test_create_kappa():
    dom = create_ortho_domain("SQUARE")
    surf = dom.get_surface("north")
    bdc = BendyDomainCreator(dom, surf)

    try:
        res = bdc.kappa_one()
        print(res)
    except InvalidPolygonError as e:
        print(e.message())
        print(e.domain.normalized_coords)
        e.domain.summarize_vectors
        e.plot()


if __name__ == "__main__":
    test_create_kappa()
