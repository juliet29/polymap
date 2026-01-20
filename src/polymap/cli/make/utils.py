import re
from pathlib import Path

from cyclopts import App
from matplotlib.figure import Figure

from polymap.geometry.layout import Layout
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


def save_figure(fig: Figure, path: Path):
    fig.set_layout_engine("constrained")
    fig.savefig(path, dpi=300)


def make_fig_save_path(
    path: Path,
    fig_name: str = "out",
):
    fig_save_path = path.parent / f"{fig_name}.png"
    return fig_save_path


def save_layout_figure(
    layout: Layout,
    path: Path,
    title: str,
    fig_name: str = "out",
    show_surfaces_labels: bool = False,
):
    case_name = get_case_name(path)
    fig, _ = plot_layout_alone(
        layout, f"{case_name} -  {title}", show_surface_labels=show_surfaces_labels
    )
    fig_save_path = make_fig_save_path(path, fig_name)
    save_figure(fig, fig_save_path)
