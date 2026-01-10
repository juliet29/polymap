from utils4plans.io import read_json
from polymap.examples.layout import layout_coords
from polymap import logconf
from polymap.json_interfaces import (
    AxGraphModel,
    LayoutModel,
    edge_data_digraph_to_model,
    layout_to_model,
)
from polymap.layout.graph import create_graph_for_all_surfaces_along_axis
from polymap.layout.interfaces import create_layout_from_dict
from rich import print
from polymap.paths import DynamicPaths

# TODO: already have some rests for this! -> tests/test_io.py


def study_axgraph_model():
    layout = create_layout_from_dict(layout_coords)
    # domains = [
    #     DomainModel(name=i.name, coords=[c.as_tuple for c in i.coords])
    #     for i in layout.domains
    # ]
    layout_model = layout_to_model(layout)
    print(layout_model.model_dump(mode="json"))

    Gax = create_graph_for_all_surfaces_along_axis(layout, "X")

    graph_model = edge_data_digraph_to_model(Gax.G)
    print(graph_model)
    print(graph_model.model_dump(mode="json"))
    # Gaxmodel = AxGraphModel(G=Gax.G, ax=Gax.ax, layout=Gax.layout)
    # print(Gaxmodel.model_dump(mode="json"))
    #
    axmodel = AxGraphModel(G=graph_model, ax=Gax.ax, layout=layout_model)
    print(axmodel.model_dump(mode="json"))

    res = axmodel.to_axgraph()
    print(res)


def study_readin_layout():
    path = DynamicPaths.example_paths / "1000.json"
    data = read_json(path)
    print(data)
    layout = LayoutModel.model_validate(data)
    print(layout)

    print(layout.to_layout())
    print(layout.model_dump_json())


if __name__ == "__main__":
    logconf.logset()
    # study_axgraph_model()
    study_readin_layout()
