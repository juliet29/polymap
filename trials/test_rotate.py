from polymap.examples.msd import get_msd_plan
from polymap.rotate.rotate import rotate_layout
from polymap.visuals.visuals import plot_layout_comparison
from math import degrees


def show_rotate():
    # id, layout = get_one_msd_layout()
    layout = get_msd_plan()
    id = "oneoff"
    angle, lay2 = rotate_layout(layout)
    plot_layout_comparison([layout, lay2], names=[id, f"r={degrees(angle)}º"])


if __name__ == "__main__":
    show_rotate()
