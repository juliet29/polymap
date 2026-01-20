from pathlib import Path
import networkx as nx
from pydantic import BaseModel, RootModel
from utils4plans.geom import coords_type_list_to_coords
from polymap.geometry.ortho import FancyOrthoDomain
from polymap.geometry.vectors import Axes
from utils4plans.geom import CoordsType
from utils4plans.io import read_json, write_json

from polymap.layout.interfaces import AxGraph, EdgeData, EdgeDataDiGraph
from polymap.geometry.layout import Layout


#  ------- Layout ---------
class LayoutModel(RootModel):
    root: dict[str, CoordsType]

    def to_layout(self):
        domains = [
            FancyOrthoDomain(coords_type_list_to_coords(v), k)
            for k, v in self.root.items()
        ]
        return Layout(domains)


def layout_to_model(layout: Layout):
    d = {i.name: [c.as_tuple for c in i.coords] for i in layout.domains}
    return LayoutModel(d)


def read_layout_from_path(path: Path):
    res = read_json(path)
    layout_model = LayoutModel.model_validate(res)
    return layout_model.to_layout()


def write_layout(layout: Layout, path: Path):
    write_json(layout_to_model(layout).model_dump(), path, OVERWRITE=True)


# ------ NetworkX Graph -----------


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
        return EdgeDataDiGraph(graph)


def edge_data_digraph_to_model(G: EdgeDataDiGraph):
    graph_dict = nx.node_link_data(G, edges="edges")

    for e in graph_dict["edges"]:
        e["data"] = e["data"].dump()

    return NetworkxGraphModel(**graph_dict)


# ------ AxGraph -----------


class AxGraphModel(BaseModel):
    G: NetworkxGraphModel
    ax: Axes
    layout: LayoutModel

    def to_axgraph(self):
        return AxGraph(self.G.to_edge_data_digraph(), self.ax, self.layout.to_layout())


def axgraph_to_model(Gax: AxGraph):
    return AxGraphModel(
        layout=layout_to_model(Gax.layout),
        ax=Gax.ax,
        G=edge_data_digraph_to_model(Gax.G),
    )
