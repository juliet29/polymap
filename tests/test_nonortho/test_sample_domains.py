from loguru import logger
import pytest
from rich.pretty import pretty_repr
from polymap.examples.domains import create_ortho_domain
from polymap.geometry.modify.validate import InvalidPolygonError
from polymap.geometry.ortho import FancyOrthoDomain
from utils4plans.logconfig import logset
from polymap.nonortho.main import orthogonalize_dom
from polymap.visuals.visuals import plot_polygon


class TestAlignSkewedDomains:
    @property
    def square_tri(self):
        return create_ortho_domain("SQUARE_TRI")

    @property
    def square_2tri(self):
        return create_ortho_domain("SQUARE_2TRI")

    @property
    def alignable_domain(self):
        return create_ortho_domain("NON_ORTHO_SQUARE")

    def plot(self, dom: FancyOrthoDomain):
        plot_polygon(dom.polygon, show=True)

    def try_align(self, dom: FancyOrthoDomain):
        plot_polygon(dom.polygon, show=True, title="starting polygon")
        try:
            new_dom = orthogonalize_dom(dom)
        except InvalidPolygonError as e:
            e.plot()
            e.message()
            logger.info(pretty_repr(e.domain.create_vector_summary))
            return
        plot_polygon(new_dom.polygon, show=True, title="final polygon")

    def test_alignment_works(self):
        dom = self.alignable_domain
        res = orthogonalize_dom(dom)
        assert res.is_orthogonal

    def test_alignment_fails(self):
        dom = self.square_tri
        with pytest.raises(InvalidPolygonError):
            res = orthogonalize_dom(dom)


if __name__ == "__main__":
    logset()
    t = TestAlignSkewedDomains()
    t.try_align(t.square_tri)
