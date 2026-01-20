from loguru import logger
from utils4plans.sets import set_equality
from utils4plans import logconfig
from utils4plans.io import read_json
from polymap.examples.layout import layout_coords
from polymap.geometry.layout import create_layout_from_dict
from polymap.layout.main.plan import create_graph_for_all_surfaces_along_axis
from polymap.paths import DynamicPaths
from polymap.pydantic_models import (
    AxGraphModel,
    LayoutModel,
    edge_data_digraph_to_model,
    layout_to_model,
)


class TestPydanticModels:
    @property
    def layout(self):
        return create_layout_from_dict(layout_coords)

    @property
    def graph_model(self):
        Gax = create_graph_for_all_surfaces_along_axis(self.layout, "X")
        return edge_data_digraph_to_model(Gax.G)

    def test_create_layout_model(self):
        model = layout_to_model(self.layout)
        res = model.model_dump(mode="json")
        assert "yellow" in res.keys()

    def test_create_graph_model(self):
        logger.debug(self.graph_model)
        res = self.graph_model.model_dump(mode="json")
        assert res["directed"]

    def test_create_axgraph_model(self):

        layout_model = layout_to_model(self.layout)
        Gax = create_graph_for_all_surfaces_along_axis(self.layout, "X")
        axmodel = AxGraphModel(G=self.graph_model, ax=Gax.ax, layout=layout_model)
        res = axmodel.model_dump(mode="json")
        assert res["G"]["directed"]


def test_layout_roundtrip():
    # test that can read layout from a file
    path = DynamicPaths.example_paths / "1000.json"
    data = read_json(path)
    logger.debug(data)
    layout_model = LayoutModel.model_validate(data)
    assert data.keys() == layout_model.root.keys()

    true_layout = layout_model.to_layout()
    assert set_equality([i.name for i in true_layout.domains], data.keys())


if __name__ == "__main__":
    logconfig.logset()
    t = TestPydanticModels()
