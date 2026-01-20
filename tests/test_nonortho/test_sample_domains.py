from loguru import logger
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


if __name__ == "__main__":
    logset()
    t = TestAlignSkewedDomains()
    t.try_align(t.square_tri)
