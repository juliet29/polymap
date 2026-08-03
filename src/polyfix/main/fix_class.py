from enum import Enum
from pathlib import Path
from typing import Callable, Literal

from utils4plans.io import make_dir, write_json

from polyfix.geometry.layout import Layout
from polyfix.layout.interfaces import AxGraph
from polyfix.layout.viz import plot_layout_with_graph_info
from polyfix.main.utils import save_figure, save_layout_figure
from polyfix.pydantic_models import axgraph_to_model, write_layout


class Stage(Enum):
    ROTATE = 0
    ORTHO = 1
    SIMPLIFY = 2
    XPLAN = 3
    XMOVE = 4
    YPLAN = 5
    YMOVE = 6
    RECONCILE = 7
    # TODO: need a level sides as well..


class PolyfixError(Exception):
    def __init__(self, stage: Stage, error: dict) -> None:
        self.stage = stage
        self.error = error

    def __dict__(self):
        return {"polyfix_stage": self.stage} | self.error


class FixBaseClass:
    def __init__(
        self,
        fix_type: Literal["Action", "Plan", "Move"],
        fx: Callable[[Layout], Layout]
        | Callable[[Layout], AxGraph]
        | Callable[[AxGraph], Layout],
        save_loc: Path,
        stage: Stage,
        save_artifacts: bool = True,
        show_fig_surface_labels: bool = False,
    ) -> None:
        self.fx = fx
        self.fix_type = fix_type
        self.save_loc = save_loc
        self.stage = stage
        self.save_artifacts = save_artifacts
        self.show_fig_surface_labels = show_fig_surface_labels

        self.save_folder = self.save_loc / self.stage.name.lower()
        make_dir(self.save_folder)

    def save_layout(self, layout: Layout):
        write_layout(layout, self.save_folder / "out.json")

        save_layout_figure(
            layout,
            path=self.save_folder,
            title=self.stage.name.capitalize(),
            show_surfaces_labels=self.show_fig_surface_labels,
        )

    def save_axgraph(self, axgraph: AxGraph):
        model = axgraph_to_model(axgraph)
        write_json(model.model_dump(), self.save_folder / "out.json")

        fig, _ = plot_layout_with_graph_info(axgraph, show=False)
        save_figure(fig, path=self.save_folder / "out.fig")

    def handle_error(self, input):
        try:
            res = self.fx(input)
        except Exception as e:
            raise PolyfixError(self.stage, e.__dict__)
        return res

    def fx_action(self, layout_: Layout) -> Layout:
        layout = self.handle_error(layout_)

        assert isinstance(layout, Layout)

        if self.save_artifacts:
            self.save_layout(layout)
        return layout

    def fx_plan(self, layout: Layout) -> AxGraph:
        axgraph = self.handle_error(layout)
        assert isinstance(axgraph, AxGraph)

        if self.save_artifacts:
            self.save_axgraph(axgraph)
        return axgraph

    def fx_move(self, axgraph: AxGraph) -> Layout:
        layout = self.handle_error(axgraph)
        assert isinstance(layout, Layout)

        if self.save_artifacts:
            self.save_layout(layout)

        return layout

    def __call__(self, input: Layout | AxGraph) -> Layout | AxGraph:
        match self.fix_type:
            case "Action":
                assert isinstance(input, Layout)
                return self.fx_action(input)
            case "Plan":
                assert isinstance(input, Layout)
                return self.fx_plan(input)
            case "Move":
                assert isinstance(input, AxGraph)
                return self.fx_move(input)

            case _:
                raise NotImplementedError
