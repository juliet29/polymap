from polymap.examples.sample_domains import create_ortho_domain
from polymap.nonortho.dot import make_ortho_coords
from rich import print
from polymap.geometry.ortho import FancyOrthoDomain
from polymap.visuals.visuals import plot_polygon
import matplotlib.pyplot as plt
from polymap.examples.msd import get_msd_plan

# from polymap.layout


def align_domain():
    dom = create_ortho_domain("NON_ORTHO_SQUARE")
    print(dom.vectors)

    coords = make_ortho_coords(dom.normalized_coords, dom.vectors)
    print(dom.normalized_coords)
    print(coords)
    new_dom = FancyOrthoDomain(coords)
    fig, (ax1, ax2) = plt.subplots(ncols=2)
    plot_polygon(dom.polygon, ax1)
    plot_polygon(new_dom.polygon, ax2)
    plt.show()


def align_msd():
    layout = get_msd_plan()

    def make_better_doms(dom: FancyOrthoDomain):
        coords = make_ortho_coords(dom.normalized_coords, dom.vectors)
        # print(dom.normalized_coords)
        # print(coords)
        return FancyOrthoDomain(coords)

    new_doms = [make_better_doms(i) for i in layout.domains]

    # fig, (ax1, ax2) = plt.subplots(ncols=2)
    # plot_polygon(sp.MultiPolygon([i.shapely_polygon for i in layout.domains]), ax1)
    # plot_polygon(sp.MultiPolygon([i.shapely_polygon for i in new_doms]), ax2)
    # plt.show()


if __name__ == "__main__":
    align_msd()
