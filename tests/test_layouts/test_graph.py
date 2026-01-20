from polymap.layout.interfaces import AxGraph, EdgeDataDiGraph, EdgeData
from loguru import logger
import networkx as nx
from utils4plans.logconfig import logset
from polymap.geometry.layout import Layout


class TestGraph:
    @property
    def Gx(self):
        g = EdgeDataDiGraph()
        delta = 2
        domain_name = "test"
        g.add_edges_from(
            [
                (1, 2, {"data": EdgeData(delta, domain_name)}),
                (1, 3, {"data": EdgeData(delta, domain_name)}),
                (4, 5, {"data": EdgeData(delta, domain_name)}),
                (4, 6, {"data": EdgeData(delta, domain_name)}),
            ]
        )
        return AxGraph(g, "X", Layout([]))

    def test_roots(self):
        assert set(self.Gx.roots) == set([1, 4])

    def test_components(self):

        components = nx.weakly_connected_components(self.Gx.G)

        logger.info(list(components))
        pass


if __name__ == "__main__":
    logset()
    t = TestGraph()
    t.test_components()
