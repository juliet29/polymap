from utils4plans.geom import CoordsType
from polymap.examples.bends import BendExamples, KappaExamples, PiExamples
import pytest
from polymap.geometry.modify.validate import validate_polygon
from polymap.geometry.ortho import FancyOrthoDomain
from polymap.visuals.visuals import plot_polygon


def test_kappa_one():
    be = BendExamples()
    dom = FancyOrthoDomain.from_tuple_list(be.kappa.one)
    validate_polygon(dom.polygon, "")


pe = PiExamples()
ke = KappaExamples()


@pytest.mark.parametrize(
    "coords", [pe.one, pe.two, pe.three, ke.one, ke.two_in, ke.two_out]
)
def test_coords(coords: CoordsType):
    dom = FancyOrthoDomain.from_tuple_list(coords)
    validate_polygon(dom.polygon, "")


if __name__ == "__main__":
    be = BendExamples()
    dom = FancyOrthoDomain.from_tuple_list(be.kappa.two_in)
    validate_polygon(dom.polygon, "")
    plot_polygon(dom.polygon, show=True)
