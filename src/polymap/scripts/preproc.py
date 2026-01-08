from pathlib import Path
from loguru import logger
from rich.pretty import pretty_repr
from utils4plans.io import write_json
from polymap import logconf
from polymap.bends.iterate2 import clean_layout
from polymap.json_interfaces import read_layout_from_path
from polymap.layout.graph import create_graph_for_all_surfaces_along_axis
from polymap.layout.interfaces import create_layout_from_dict
from polymap.layout.visuals import plot_layout_with_graph_info
from polymap.process.process import make_ortho_layout
from polymap.rotate.rotate import rotate_layout
from cyclopts import App
from polymap.examples.layout import example_layouts
from polymap.paths import DynamicPaths
import re

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
def rotate(path: Path):
    in_layout = read_layout_from_path(path)

    angle, layout = rotate_layout(in_layout)
    logger.info(f"{angle=}")

    return layout.dump()


@app.command()
def ortho(path: Path):
    in_layout = read_layout_from_path(path)
    layout = make_ortho_layout(in_layout)
    return layout.dump()


@app.command()
def simplify(path: Path):
    in_layout = read_layout_from_path(path)
    layout, bad_doms = clean_layout(in_layout, get_case_name(path))
    if bad_doms:
        logger.warning(
            f"Bad domains exist which may cause problems: {pretty_repr(bad_doms)}"
        )
    return layout.dump()


@app.command()
def pull(path: Path, fig_save_path: Path):
    in_layout = read_layout_from_path(path)
    Gx = create_graph_for_all_surfaces_along_axis(in_layout, "X")
    fig, ax = plot_layout_with_graph_info(Gx, get_case_name(path), show=False)
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
