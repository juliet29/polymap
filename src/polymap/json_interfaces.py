from pathlib import Path
import networkx as nx
from pydantic import TypeAdapter, BaseModel, RootModel
from utils4plans.geom import Coord, coords_type_list_to_coords
from polymap.geometry.ortho import FancyOrthoDomain
from polymap.geometry.vectors import Axes
from polymap.interfaces import CoordsType
from utils4plans.io import read_json

from polymap.layout.graph import AxGraph, EdgeData
from polymap.layout.interfaces import Layout


layout_type_adapter = TypeAdapter(dict[str, CoordsType])


class DomainModel(BaseModel):
    name: str
    coords: list[tuple[float, float]]

    def to_domain(self):
        coords = [Coord(*i) for i in self.coords]
        return FancyOrthoDomain(coords, self.name)


class LayoutModel(RootModel):
    root: dict[str, CoordsType]

    def to_layout(self):
        domains = [
            FancyOrthoDomain(coords_type_list_to_coords(v), k)
            for k, v in self.root.items()
        ]
        return Layout(domains)


class NodeModel(BaseModel):
    id: str


class EdgeDataModel(BaseModel):
    delta: float
    domain_name: str

    def to_edge_data(self):
        return EdgeData(self.delta, self.domain_name)


class EdgeModel(BaseModel):
    source: str
    target: str
    data: EdgeDataModel

    def to_edge_data_edges(self):
        data = self.model_dump(mode="json")
        data["data"] = self.data.to_edge_data()
        return data


class NetworkxGraphModel(BaseModel):
    directed: bool
    multigraph: bool
    nodes: list[NodeModel]
    edges: list[EdgeModel]
    graph: dict = dict()

    def to_edge_data_digraph(self):
        data = self.model_dump(mode="json")
        data["edges"] = [i.to_edge_data_edges() for i in self.edges]

        graph = nx.node_link_graph(data, edges="edges")
        return graph


def read_layout_from_path(path: Path):
    res = read_json(path)
    layout_input = layout_type_adapter.validate_python(res)
    domains: list[FancyOrthoDomain] = []
    for k, v in layout_input.items():
        domain = FancyOrthoDomain.from_tuple_list(v)
        domain.set_name(k)
        domains.append(domain)

    return Layout(domains)


class AxGraphModel(BaseModel):
    G: NetworkxGraphModel
    ax: Axes
    layout: LayoutModel

    def to_axgraph(self):
        return AxGraph(self.G.to_edge_data_digraph(), self.ax, self.layout.to_layout())
