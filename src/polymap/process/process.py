from typing import Any, Protocol, get_args

import shapely as sp
from loguru import logger

from polymap.bends.main import remove_bends_from_layout
from polymap.config import TOLERANCE
from polymap.examples.msd import MSD_IDs, get_one_msd_layout
from polymap.geometry.ortho import FancyOrthoDomain
from polymap.geometry.shapely_helpers import get_coords_from_shapely_polygon
from polymap.geometry.vectors import Axes
from polymap.interfaces import GraphPairs
from polymap.layout.graph import create_graph_for_all_surfaces_along_axis
from polymap.layout.interfaces import Layout
from polymap.layout.update import create_updated_layout
from polymap.nonortho.dot import make_ortho_coords
from polymap.process.interfaces import ProcessGraphPairs, ProcessLayouts
from polymap.process.viz import make_study_plot
from polymap.rotate.main import rotate_layout


def simplify_layout_shapely(layout: Layout, tolerance: float = TOLERANCE):
    def simplify_domain(dom: FancyOrthoDomain):
        simple_poly = sp.simplify(dom.polygon, tolerance=tolerance)
        simple_dom = FancyOrthoDomain(get_coords_from_shapely_polygon(simple_poly))

        ortho_coords = make_ortho_coords(simple_dom.coords, simple_dom.vectors)

        ortho_dom = FancyOrthoDomain(ortho_coords, dom.name)
        return ortho_dom

    new_doms = [simplify_domain(i) for i in layout.domains]
    return Layout(new_doms)


def simplify_layout(layout: Layout, id: str = "", tolerance: float = TOLERANCE):
    new_layout, bad_domains = remove_bends_from_layout(layout, layout_id=id)
    return new_layout


def make_ortho_layout(layout: Layout):

    def make_ortho_doms(dom: FancyOrthoDomain):
        if not dom.is_orthogonal:

            logger.log("START", f"Resolving non-ortho on {dom.name}")
            coords = make_ortho_coords(dom.normalized_coords, dom.vectors)

            new_dom = FancyOrthoDomain(coords, name=dom.name)
            try:
                assert new_dom.is_orthogonal
            except AssertionError:
                raise RuntimeError(
                    f"Failed to ortho domain {new_dom.name}: {new_dom.create_vector_summary}"
                )
            logger.log("END", f"Finished resolving non-ortho on {dom.name}\n")
            return new_dom

        logger.trace(f"No non-ortho on {dom.name}\n")
        return dom

    new_doms = map(lambda x: make_ortho_doms(x), layout.domains)
    return Layout(list(new_doms))


class ReturnsLayout(Protocol):
    def __call__(self, *args: Any, **kwds: Any) -> Layout: ...


def prep_study_plot(
    msd_id: str, layouts: list[Layout], graph_pairs: list[GraphPairs], show_plot
):
    pl = ProcessLayouts(msd_id, *layouts)
    pgp = ProcessGraphPairs(*graph_pairs)
    if show_plot:
        make_study_plot(pl, pgp)


class LayoutProcessFailure(Exception):
    def __init__(self, message: str) -> None:
        self.message = message


def process_layout(
    msd_id: MSD_IDs | None = None,
    layout: Layout | None = None,
    other_layout_id: str = "",
    rotate: bool = True,
    ortho: bool = True,
    show_plot=False,
):
    layout_id = msd_id if msd_id else other_layout_id

    def attempt(fx: ReturnsLayout, *args: Any, **kwargs: Any):
        try:
            layout = fx(*args, **kwargs)
        except Exception as e:
            prep_study_plot(layout_id, layouts, graph_pairs, show_plot)
            raise LayoutProcessFailure(
                f"failed to finish processing layout for {layout_id}.\n {e}"
            )

        return layout

    def attempt_make_graph(layout: Layout, axes: Axes):
        try:
            axgraph = create_graph_for_all_surfaces_along_axis(layout, axes)
        except (AssertionError, ValueError, Exception) as e:
            prep_study_plot(layout_id, layouts, graph_pairs, show_plot)
            raise LayoutProcessFailure(
                f"failed to make {axes} graph {layout_id}.\n {e}"
            )

        return axgraph

    layouts = []
    graph_pairs = []

    if not layout:
        assert msd_id and msd_id in get_args(
            MSD_IDs
        ), f"MSD IDs {msd_id} is not expected.."
        _, layout = get_one_msd_layout(msd_id)

    if rotate and ortho:
        angle, rotated_layout = rotate_layout(layout)
        logger.trace(f"Rotated layout by {angle}")
        layouts.extend([layout, rotated_layout])

        ortho_layout = attempt(make_ortho_layout, rotated_layout)
        layouts.append(ortho_layout)
    else:
        ortho_layout = layout

    layout_id = msd_id if msd_id else other_layout_id

    simple_layout = attempt(simplify_layout, ortho_layout, id=layout_id)
    layouts.append(simple_layout)

    Gx = attempt_make_graph(simple_layout, "X")
    graph_pairs.append(Gx.nb_pairs)

    layx = attempt(create_updated_layout, Gx)
    layouts.append(layx)
    #
    Gy = attempt_make_graph(layx, "Y")
    graph_pairs.append(Gy.nb_pairs)

    layy = attempt(create_updated_layout, Gy)
    layouts.append(layy)
    prep_study_plot(layout_id, layouts, graph_pairs, show_plot)
    # logger.success(f"[green]Finished process layout for {layout_id}")

    return layy
