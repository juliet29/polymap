from polymap.examples.msd import get_one_msd_layout
from polymap.layout.graph import create_graph_for_layout
from polymap.layout.interfaces import Layout
from polymap.layout.update import collect_updated_domains

# from polymap.visuals import plot_graph_pairs_on_layout, plot_layout


# test plotting a layout and seeing if can get the name labels
# test plotting a layout and see if can get surface labels
# test and see if can get surface colors..
#


def test_plotting_layout_with_labels():
    id, layout = get_one_msd_layout()
    layout.surface_summary

    # ax = plot_layout(layout, layout_name=id, show=True)
    Gx, Gy = create_graph_for_layout(layout)
    up_doms = collect_updated_domains(Gx)
    Layout(up_doms).domain_names
    #
    # ax = plot_layout(layout, layout_name=id, show=False)
    # ax = plot_graph_pairs_on_layout(layout, Gx.nb_pairs, ax, show=True)

    #  layx = get_new_doms_for_graph(Gx)
    # ax = plot_layout(layx, layout_name=id, show=True)
    #
    # return layx

    pass

    return Gx, Gy


if __name__ == "__main__":
    res = test_plotting_layout_with_labels()
