from polymap.examples.msd import get_one_msd_layout
import shapely as sp
from polymap.visuals import plot_layout


# test plotting a layout and seeing if can get the name labels
# test plotting a layout and see if can get surface labels
# test and see if can get surface colors..
#


def test_plotting_layout_with_labels():
    id, layout = get_one_msd_layout()

    polygons = sp.MultiPolygon([i.polygon for i in layout.domains])
    plot_layout(layout, layout_name=id)

    pass


if __name__ == "__main__":
    test_plotting_layout_with_labels()
