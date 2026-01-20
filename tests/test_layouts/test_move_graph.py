from utils4plans.sets import set_equality
from utils4plans import logconfig
from loguru import logger
from polymap.examples.layout import smart_graph_example
from polymap.layout.main.plan import (
    create_graph_for_all_surfaces_along_axis,
    create_move_graph,
    Edge,
    EdgeData,
)
from polymap.geometry.layout import create_layout_from_dict
from polymap.visuals.visuals import plot_layout


class TestSmartGraph:
    layout = create_layout_from_dict(smart_graph_example)

    def show_layout(self):
        plot_layout(self.layout, show=True)

    def test_smart_graph(self):
        Gax = create_graph_for_all_surfaces_along_axis(self.layout, "X")
        logger.info(Gax.G.edge_data())

        G2 = create_move_graph(self.layout, Gax.G)

        expected = [
            Edge(
                u="C-west_0", v="A-east_0", data=EdgeData(delta=-1.0, domain_name="C")
            ),
            Edge(u="A-east_0", v="B-west_0", data=EdgeData(delta=1.0, domain_name="A")),
        ]
        logger.info(G2.edge_data())
        assert set_equality(expected, G2.edge_data())


if __name__ == "__main__":
    logconf.logset()
    t = TestSmartGraph()
    t.test_smart_graph()
