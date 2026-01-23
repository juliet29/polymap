import math
from pathlib import Path

from cyclopts import App
from loguru import logger
from rich.pretty import pretty_repr
from utils4plans.io import read_json, write_json

from polymap.bends.main import remove_bends_from_layout
from polymap.cli.make.utils import (
    get_case_name,
    make_fig_save_path,
    save_figure,
    save_layout_figure,
)
from polymap.geometry.modify.precision import decrease_layout_precision
from polymap.geometry.modify.validate import InvalidPolygonError
from polymap.geometry.vectors import Axes
from polymap.layout.main.move import try_moves
from polymap.layout.main.plan import create_move_graph_for_all_surfaces_along_axis
from polymap.layout.viz import plot_layout_with_graph_info
from polymap.nonortho.main import orthogonalize_layout
from polymap.pydantic_models import (
    AxGraphModel,
    axgraph_to_model,
    layout_to_model,
    read_layout_from_path,
    write_layout,
)
from polymap.rotate.main import rotate_layout

make_app = App(name="make")


@make_app.command()
def rotate(path: Path, out_path: Path):
    in_layout = read_layout_from_path(path)
    save_layout_figure(in_layout, out_path, "Input", "in")

    angle_radians, layout = rotate_layout(in_layout)
    angle_degrees = math.degrees(angle_radians)
    logger.info(f"{angle_degrees=}")
    logger.info(f"{angle_radians=}")
    save_layout_figure(layout, out_path, f"Rotated by {angle_degrees:.2f}º")
    write_layout(layout, out_path)


@make_app.command()
def ortho(path: Path, out_path: Path):
    in_layout = read_layout_from_path(path)
    try:
        layout = orthogonalize_layout(in_layout)

        # TODO: make formal error class
    except InvalidPolygonError as e:
        e.message()
        raise RuntimeError(
            "Could not orthogonalize the layout due to at least one polygon being non-orthogonalizable"
        )
    save_layout_figure(layout, out_path, "Orthoginalized")
    write_layout(layout, out_path)


@make_app.command()
def simplify(path: Path, out_path: Path):
    in_layout = read_layout_from_path(path)
    layout, bad_doms = remove_bends_from_layout(in_layout, get_case_name(path))
    if bad_doms:
        logger.warning(
            f"Bad domains exist which may cause problems: {pretty_repr(bad_doms)}"
        )
    layout = decrease_layout_precision(layout)
    save_layout_figure(layout, out_path, "Simplified", show_surfaces_labels=True)
    write_json(layout_to_model(layout).model_dump(), out_path)


@make_app.command()
def plan(ax: Axes, path: Path, out_path: Path):
    in_layout = read_layout_from_path(path)
    Gax = create_move_graph_for_all_surfaces_along_axis(in_layout, ax)

    fig, _ = plot_layout_with_graph_info(
        Gax, f"{get_case_name(path)} {ax}-Plan", show=False
    )
    save_figure(fig, make_fig_save_path(path))

    Gax_model = axgraph_to_model(Gax)
    write_json(Gax_model.model_dump(), out_path, OVERWRITE=True)


@make_app.command()
def move(ax: Axes, path: Path, out_path: Path):
    Gax = AxGraphModel.model_validate(read_json(path)).to_axgraph()
    layout = try_moves(Gax)
    save_layout_figure(layout, out_path, title=f"{ax}-Move")
    write_layout(layout, out_path)
