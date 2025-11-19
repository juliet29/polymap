from polymap.examples.msd import get_one_msd_layout
from polymap.layout.graph import collect_node_nbs, create_graph_for_layout
from polymap.visuals import plot_graph_pairs_on_layout, plot_layout


# test plotting a layout and seeing if can get the name labels
# test plotting a layout and see if can get surface labels
# test and see if can get surface colors..
#


def test_plotting_layout_with_labels():
    id, layout = get_one_msd_layout()
    Gx, Gy = create_graph_for_layout(layout)
    gpairs_x = collect_node_nbs(Gx.G)

    ax = plot_layout(layout, layout_name=id, show=False)
    ax = plot_graph_pairs_on_layout(layout, gpairs_x, ax, show=True)

    pass


if __name__ == "__main__":
    test_plotting_layout_with_labels()
