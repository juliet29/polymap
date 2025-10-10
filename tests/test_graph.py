import networkx as nx
from polymap.layout.graph import AxGraph


def create_Gx():
    g = nx.DiGraph()
    g.add_edges_from(
        [
            (1, 2, {"data": "a"}),
            (1, 3, {"data": "b"}),
            (4, 5, {"data": "c"}),
            (4, 6, {"data": "d"}),
        ]
    )
    return AxGraph(g, "X")


def test_graph():
    Gx = create_Gx()
    assert set(Gx.roots) == set([1,4])



if __name__ == "__main__":
    test_graph()