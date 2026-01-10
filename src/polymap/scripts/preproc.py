from pathlib import Path
from loguru import logger
from rich.pretty import pretty_repr
from utils4plans.io import read_json, write_json
from polymap import logconf
from polymap.bends.iterate2 import clean_layout
from polymap.json_interfaces import (
    AxGraphModel,
    axgraph_to_model,
    layout_to_model,
    read_layout_from_path,
)
from polymap.layout.graph import create_move_graph_for_all_surfaces_along_axis
from polymap.layout.interfaces import create_layout_from_dict
from polymap.layout.u2 import try_moves
from polymap.layout.visuals import plot_layout_with_graph_info
from polymap.process.process import make_ortho_layout
from polymap.rotate.rotate import rotate_layout
from cyclopts import App
from polymap.examples.layout import example_layouts
from polymap.paths import DynamicPaths
import re

from polymap.visuals.visuals import plot_layout_alone


app = App()


def get_case_name(path: Path):
    pattern = re.compile(r"\d{3,}")
    match_object = pattern.search(str(path))
    if match_object:
        return match_object.group()
    else:
        return path.stem


@app.command()
def generate_examples():
    for ix, coords in enumerate(example_layouts):
        layout = create_layout_from_dict(coords)
        path = DynamicPaths.example_paths / f"{1000 + ix}.json"
        write_json(layout.dump(as_string=False), path, OVERWRITE=True)


@app.command()
def rotate(path: Path, json_save_path: Path):
    in_layout = read_layout_from_path(path)

    angle, layout = rotate_layout(in_layout)
    logger.info(f"{angle=}")

    return write_json(layout_to_model(layout).model_dump(), json_save_path)


@app.command()
def ortho(path: Path, json_save_path: Path):
    in_layout = read_layout_from_path(path)
    layout = make_ortho_layout(in_layout)
    return write_json(layout_to_model(layout).model_dump(), json_save_path)


@app.command()
def simplify(path: Path, json_save_path: Path):
    in_layout = read_layout_from_path(path)
    layout, bad_doms = clean_layout(in_layout, get_case_name(path))
    if bad_doms:
        logger.warning(
            f"Bad domains exist which may cause problems: {pretty_repr(bad_doms)}"
        )
    return write_json(layout_to_model(layout).model_dump(), json_save_path)


@app.command()
def xplan(path: Path, fig_save_path: Path, json_save_path: Path):
    in_layout = read_layout_from_path(path)
    Gx = create_move_graph_for_all_surfaces_along_axis(in_layout, "X")

    case_name = get_case_name(path)

    fig, _ = plot_layout_with_graph_info(Gx, case_name, show=False)
    fig.set_layout_engine("constrained")
    fig.savefig(fig_save_path, dpi=300)

    Gax_model = axgraph_to_model(Gx)
    write_json(Gax_model.model_dump(), json_save_path)


@app.command()
def xmove(path: Path, fig_save_path: Path, json_save_path: Path):
    # TODO: put into its own function..
    Gx = AxGraphModel.model_validate(read_json(path)).to_axgraph()

    layx = try_moves(Gx)
    write_json(layx.dump(as_string=False), json_save_path, OVERWRITE=True)
    case_name = get_case_name(path)

    fig, _ = plot_layout_alone(layx, f"{case_name} X-Pull", show_surface_labels=True)
    fig.set_layout_engine("constrained")
    fig.savefig(fig_save_path, dpi=300)


@app.command()
def welcome():
    return "Hello old friend"


def main():
    logconf.logset()
    app()


if __name__ == "__main__":
    main()
