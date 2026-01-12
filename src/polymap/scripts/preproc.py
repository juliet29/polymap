import re
import math
from pathlib import Path

from cyclopts import App
from loguru import logger
from rich.pretty import pretty_repr
from utils4plans.io import read_json, write_json

from polymap import logconf
from polymap.bends.iterate2 import clean_layout
from polymap.examples.layout import example_layouts
from polymap.geometry.modify.validate import InvalidPolygonError
from polymap.geometry.vectors import Axes
from polymap.json_interfaces import (
    AxGraphModel,
    axgraph_to_model,
    layout_to_model,
    read_layout_from_path,
)
from polymap.layout.graph import create_move_graph_for_all_surfaces_along_axis
from polymap.layout.interfaces import Layout, create_layout_from_dict
from polymap.layout.u2 import try_moves
from polymap.layout.visuals import plot_layout_with_graph_info
from polymap.nonortho.main import orthogonalize_layout
from polymap.paths import DynamicPaths
from polymap.rotate.rotate import rotate_layout
from polymap.visuals.visuals import plot_layout_alone

# TODO: clean up imports to clean up project structure

app = App()


def get_case_name(path: Path):
    pattern = re.compile(r"\d{3,}")
    match_object = pattern.search(str(path))
    if match_object:
        return match_object.group()
    else:
        return path.stem


def get_path_parent(path: Path):
    return path.parent


def save_layout(layout: Layout, path: Path, title: str, fig_name: str = "out"):
    case_name = get_case_name(path)
    fig, _ = plot_layout_alone(
        layout, f"{case_name} -  {title}", show_surface_labels=False
    )
    fig.set_layout_engine("constrained")
    fig_save_path = path.parent / f"{fig_name}.png"
    fig.savefig(fig_save_path, dpi=300)


@app.command()
def generate_examples():
    for ix, coords in enumerate(example_layouts):
        layout = create_layout_from_dict(coords)
        path = DynamicPaths.example_paths / f"{1000 + ix}.json"
        write_json(layout.dump(as_string=False), path, OVERWRITE=True)


@app.command()
def rotate(path: Path, json_save_path: Path):
    in_layout = read_layout_from_path(path)
    save_layout(in_layout, json_save_path, "Input", "in")

    angle_radians, layout = rotate_layout(in_layout)
    angle_degrees = math.degrees(angle_radians)
    logger.info(f"{angle_degrees=}")
    logger.info(f"{angle_radians=}")
    save_layout(layout, json_save_path, f"Rotated by {angle_degrees:.2f}º")

    write_json(layout_to_model(layout).model_dump(), json_save_path)


@app.command()
def ortho(path: Path, json_save_path: Path):
    in_layout = read_layout_from_path(path)
    try:
        layout = orthogonalize_layout(in_layout)
    # NOTE: this will fail  if any domain cannot be orthogonalized and will not produce a json
    except InvalidPolygonError as e:
        e.message()
        return
    save_layout(layout, json_save_path, "Orthoginalized")

    write_json(layout_to_model(layout).model_dump(), json_save_path, OVERWRITE=True)


@app.command()
def simplify(path: Path, fig_save_path: Path, json_save_path: Path):
    in_layout = read_layout_from_path(path)
    layout, bad_doms = clean_layout(in_layout, get_case_name(path))
    if bad_doms:
        logger.warning(
            f"Bad domains exist which may cause problems: {pretty_repr(bad_doms)}"
        )

    case_name = get_case_name(path)
    fig, _ = plot_layout_alone(
        layout, f"{case_name} Simplified", show_surface_labels=True
    )
    fig.set_layout_engine("constrained")
    fig.savefig(fig_save_path, dpi=300)

    write_json(layout_to_model(layout).model_dump(), json_save_path)


@app.command()
def plan(ax: Axes, path: Path, fig_save_path: Path, json_save_path: Path):
    in_layout = read_layout_from_path(path)
    Gax = create_move_graph_for_all_surfaces_along_axis(in_layout, ax)

    case_name = get_case_name(path)

    fig, _ = plot_layout_with_graph_info(Gax, f"{case_name} {ax}-Plan", show=False)
    fig.set_layout_engine("constrained")
    fig.savefig(fig_save_path, dpi=300)

    Gax_model = axgraph_to_model(Gax)
    write_json(Gax_model.model_dump(), json_save_path, OVERWRITE=True)


@app.command()
def move(ax: Axes, path: Path, fig_save_path: Path, json_save_path: Path):
    Gax = AxGraphModel.model_validate(read_json(path)).to_axgraph()

    layout = try_moves(Gax)
    case_name = get_case_name(path)

    fig, _ = plot_layout_alone(
        layout, f"{case_name} {ax}-Move", show_surface_labels=False
    )
    fig.set_layout_engine("constrained")
    fig.savefig(fig_save_path, dpi=300)

    write_json(layout.dump(as_string=False), json_save_path, OVERWRITE=True)


@app.command()
def welcome():
    return "Welcome to polymap"


def main():
    logconf.logset()
    app()


if __name__ == "__main__":
    main()
