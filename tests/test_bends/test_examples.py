from loguru import logger
import pytest
from utils4plans.geom import CoordsType
from polymap.bends.bends import assign_bends
from polymap.examples.bends import BendExamples
from polymap.bends.interfaces import BendListSummary
from polymap.bends.main import remove_all_bends_from_domain
from polymap.examples.msd import MSDDomain, MSDDomainName
from polymap.geometry.ortho import FancyOrthoDomain
from utils4plans.logconfig import logset


def study_make_bends_all():
    be = BendExamples()
    for dom in be.all_doms:
        logger.info(f"[bold blue]Starting assignment for [red]{dom.name}[/red]")
        bh = assign_bends(dom)
        logger.info(bh.summary_str)


def study_one_bend():
    coords = BendExamples().pi.three
    dom = FancyOrthoDomain.from_tuple_list(coords, "pi3")
    # plot_polygon(dom.polygon, show=True)
    bh = assign_bends(dom)
    logger.debug(bh.pi3s[0].study_vectors())
    logger.debug(bh.pi3s[0].are_vectors_correct)


def study_move(coords: CoordsType, dom_name: str):
    dom = FancyOrthoDomain.from_tuple_list(coords, dom_name)
    msd_dom = MSDDomainName(0, dom_name)  # pyright: ignore[reportArgumentType]
    res = remove_all_bends_from_domain(
        MSDDomain(msd_dom, dom),
        show_failure=True,
        show_complete_iteration=False,  # NOTE: change to true if want to actually see!
    )
    assert res


class TestBendMoves:
    def test_pi1(self):
        study_move(BendExamples.pi.one, "pi1")

    def test_pi2(self):
        study_move(BendExamples.pi.two, "pi2")

    def test_pi3(self):
        study_move(BendExamples.pi.three, "pi3")

    def test_kappa1(self):
        study_move(BendExamples.kappa.one, "kappa1")

    def test_kappa2in(self):
        study_move(BendExamples.kappa.two_in, "kappa_two_in")

    def test_kappa2out(self):
        study_move(BendExamples.kappa.two_out, "kappa_two_out")


class TestBendExamples:
    keys = ["kappas", "kappa2s", "kappa2s", "pis", "pi2s", "pi3s"]
    inp = [(i, j) for i, j in zip(BendExamples().all_doms, keys)]

    @pytest.mark.parametrize("domain, key", inp)
    def test_bends(self, domain: FancyOrthoDomain, key: str):

        bh = assign_bends(domain)
        res = bh.summary[key]

        assert isinstance(res, BendListSummary)

        assert res.size == 1

    @pytest.mark.parametrize("domain, key", inp)
    def test_passing(self, domain: FancyOrthoDomain, key: str):

        bh = assign_bends(domain)
        res = bh.summary[key]

        assert isinstance(res, BendListSummary)

        assert res.n_passing == 1


if __name__ == "__main__":
    logset()
    t = TestBendMoves()
    t.test_kappa2out()
