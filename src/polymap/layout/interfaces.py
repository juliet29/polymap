import networkx as nx
from polymap.geometry.layout import Layout
from polymap.geometry.vectors import Axes
from dataclasses import dataclass
from typing import NamedTuple

GraphPairs = dict[str, list[str]]


def collect_nbs(G: nx.DiGraph) -> GraphPairs:
    nb_dict = {}
    for e in G.edges:
        e1, e2 = e
        if e1 not in nb_dict.keys():
            nb_dict[e1] = []
            nb_dict[e1].append(e2)
        else:
            nb_dict[e1].append(e2)

    return nb_dict


class EdgeData(NamedTuple):
    delta: float
    domain_name: str

    def dump(self):
        return self._asdict()


class Edge(NamedTuple):
    u: str
    v: str
    data: EdgeData

    def summary_string(self, short: bool = False):
        edge = (self.u, self.v)
        delta = float(f"{self.data.delta:.2f}") if short else self.data.delta
        s = {edge: delta}
        return s


class EdgeDataDiGraph(nx.DiGraph):
    def edge_data(self):
        res = list(self.edges(data=True))
        return [Edge(i[0], i[1], i[2]["data"]) for i in res]

    def edge_summary_list(self):
        strs = [e.summary_string() for e in self.edge_data()]
        return strs


@dataclass
class AxGraph:
    G: EdgeDataDiGraph
    ax: Axes
    layout: Layout

    def get_delta(self, nb1: str, nb2: str):
        for nb in [nb1, nb2]:
            assert nb in self.G.nodes

        return self.G.edges[(nb1, nb2)]["data"].delta

    def get_neighors(self, node: str):
        return list(self.G.neighbors(node))

    @property
    def roots(self):
        return [n[0] for n in self.G.in_degree if n[1] == 0]

    @property
    def domains(self):
        return self.layout.domains

    @property
    def nb_pairs(self):
        return collect_nbs(self.G)
