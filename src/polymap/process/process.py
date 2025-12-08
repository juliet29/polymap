from typing import Any, Protocol, get_args


import shapely as sp

from polymap.bends.iterate import clean_layout
from polymap.examples.msd import MSD_IDs, get_one_msd_layout
from polymap.geometry.ortho import FancyOrthoDomain
from polymap.geometry.shapely_helpers import get_coords_from_shapely_polygon
from polymap.geometry.vectors import Axes
from polymap.interfaces import GraphPairs
from polymap.layout.interfaces import Layout
from polymap.layout.graph import create_graph_for_all_surfaces_along_axis
from polymap.layout.update import create_updated_layout
from polymap.nonortho.dot import make_ortho_coords
from polymap.process.interfaces import ProcessGraphPairs, ProcessLayouts
from polymap.process.viz import make_study_plot
from polymap.rotate.rotate import rotate_layout


TOLERANCE = 0.15


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
    new_layout, bad_domains = clean_layout(layout, layout_id=id)
    return new_layout


class ReturnsLayout(Protocol):
    def __call__(self, *args: Any, **kwds: Any) -> Layout: ...


def prep_study_plot(msd_id: str, layouts: list[Layout], graph_pairs: list[GraphPairs]):
    pl = ProcessLayouts(msd_id, *layouts)
    pgp = ProcessGraphPairs(*graph_pairs)
    make_study_plot(pl, pgp)


def process_layout(msd_id: MSD_IDs, layout: Layout | None = None):

    def attempt(fx: ReturnsLayout, *args: Any, **kwargs: Any):
        try:
            layout = fx(*args, **kwargs)
        except Exception as e:
            print(f"failed to finish processing {msd_id}.\n {e}")
            prep_study_plot(msd_id, layouts, graph_pairs)

            raise Exception("Failed to generate layout")

        return layout

    def attempt_make_graph(layout: Layout, axes: Axes):
        try:
            axgraph = create_graph_for_all_surfaces_along_axis(layout, axes)
        except (AssertionError, ValueError, Exception) as e:
            err = f"failed to make {axes} graph for {msd_id}.\n {e}"
            print(err)
            prep_study_plot(msd_id, layouts, graph_pairs)

            raise Exception(err)

        return axgraph

    layouts = []
    graph_pairs = []

    if not layout:
        assert msd_id in get_args(MSD_IDs), f"MSD IDs {msd_id} is not expected.."
        _, layout = get_one_msd_layout(msd_id)

    rotated_layout = rotate_layout(layout)
    # ortho layout

    simple_layout = attempt(simplify_layout, layout, id=msd_id)
    layouts.extend([layout, simple_layout])

    Gx = attempt_make_graph(simple_layout, "X")
    graph_pairs.append(Gx.nb_pairs)

    layx = attempt(create_updated_layout, Gx)
    layouts.append(layx)
    #
    Gy = attempt_make_graph(layx, "Y")
    graph_pairs.append(Gy.nb_pairs)

    layy = attempt(create_updated_layout, Gy)
    layouts.append(layy)
    prep_study_plot(msd_id, layouts, graph_pairs)

    return msd_id
