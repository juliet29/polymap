from loguru import logger
import pytest
import shapely
from utils4plans.logconfig import logset
from polymap.examples.layout import gen_square
from polymap.geometry.ortho import FancyOrthoDomain
from polymap.geometry.shapely_helpers import decrease_precision
from polymap.layout.interfaces import Layout
from polymap.visuals.visuals import plot_layout


class TestPrecisionInteraction:
    ETA = 5 / 7
    SIZE = 1
    HEIGHT = 10

    SQUARE_1_START = 1 + ETA
    SQUARE_1_TL = (SQUARE_1_START, HEIGHT)

    DIFF = ETA / 100
    SQUARE_2_TL = (SQUARE_1_START + DIFF + SIZE, HEIGHT)

    @property
    def sq1(self):
        with logger.contextualize(sq=1):
            coords = gen_square(self.SQUARE_1_TL, self.SIZE)
        return FancyOrthoDomain.from_tuple_list(coords, "sq1")

    @property
    def sq2(self):
        with logger.contextualize(sq=2):
            coords = gen_square(self.SQUARE_2_TL, self.SIZE)
        return FancyOrthoDomain.from_tuple_list(coords, "sq2")

    def show(self):
        layout = Layout([self.sq1, self.sq2])
        # layout = Layout([self.sq2])
        plot_layout(layout)

    def setup(self, prec: int):
        s1, s2 = self.sq1.polygon, self.sq2.polygon
        relate1 = shapely.relate(s1, s2)
        r1, r2 = [decrease_precision(i, prec) for i in [s1, s2]]
        relate2 = shapely.relate(r1, r2)
        return relate1, relate2

    def test_decrease_precision_gap_remains(self):
        prec = 3
        rel1, rel2 = self.setup(prec)
        assert rel1 == rel2

    def test_decrease_precision_gap_removed(self):
        prec = 1
        rel1, rel2 = self.setup(prec)
        with pytest.raises(AssertionError):
            assert rel1 == rel2


if __name__ == "__main__":
    logset()
    t = TestPrecisionInteraction()
    # t.test_decrease_precision()
