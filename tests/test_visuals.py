from polymap.examples.msd import get_one_msd_layout

from polymap.layout.update import create_updated_layout
from polymap.layout.graph import (
    create_graph_for_layout,
    AxGraph,
    create_graph_for_all_surfaces_along_axis,
)
from polymap.visuals import plot_layout, plot_graph_pairs_on_layout


# test plotting a layout and seeing if can get the name labels
# test plotting a layout and see if can get surface labels
# test and see if can get surface colors..
#


def test_plotting_layout_with_labels():
    id, layout = get_one_msd_layout("71308")
    layout.surface_summary

    # ax = plot_layout(layout, layout_name=id, show=True)
    Gx, _ = create_graph_for_layout(layout)
    # up_doms = collect_updated_domains(Gx)
    # Layout(up_doms).domain_names
    #
    ax = plot_layout(layout, layout_name=id, show=True)
    # ax = plot_graph_pairs_on_layout(layout, Gx.nb_pairs, ax, show=True, alpha=0.7)

    layx = create_updated_layout(Gx)
    Gy = create_graph_for_all_surfaces_along_axis(layx, "Y")
    ax = plot_layout(layx, layout_name=id, show=False)
    ax = plot_graph_pairs_on_layout(layout, Gy.nb_pairs, ax, show=True, alpha=0.7)
    layy = create_updated_layout(AxGraph(Gy.G, "Y", layx))

    ax = plot_layout(layy, layout_name=id, show=True)
    #
    # return layx

    layx.domain_names

    # return Gx, Gy


if __name__ == "__main__":
    res = test_plotting_layout_with_labels()
