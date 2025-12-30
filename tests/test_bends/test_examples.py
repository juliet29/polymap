from loguru import logger
import pytest
from polymap.bends.b2 import assign_bends
from polymap.bends.examples import BendExamples
from polymap.bends.i2 import BendListSummary
from polymap.geometry.ortho import FancyOrthoDomain
from polymap.logconf import logset


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
    study_one_bend()
    # study_make_bends_all()

    # t.test_bends()
