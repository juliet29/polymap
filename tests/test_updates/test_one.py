from polymap.layout.interfaces import create_layout_from_json
from polymap.geometry.ortho import FancyOrthoDomain
from utils4plans.geom import Coord
import shapely as sp
import matplotlib.pyplot as plt
from rich import print
from polymap.visuals import plot_polygon
from polymap.examples.sample_domains import create_ortho_domain
from polymap.interfaces import PairedCoord


def plot_two(dom, new_dom):
    fig, (ax1, ax2) = plt.subplots(ncols=2)
    plot_polygon(dom.shapely_polygon, ax1)
    plot_polygon(new_dom.shapely_polygon, ax2)
    plt.show()


def test_moving_surface():
    layout = create_layout_from_json("48205")
    dom = layout.get_domain("room_7")
    print(dom.is_orthogonal)

    # print(dom.surfaces)
    new_dom = dom.update_surface(dom.get_surface("east", 1), 2.822)
    # plot_two(dom, new_dom)
    print(dom.normalized_coords)


def check_recreating_geom():
    dom = create_ortho_domain("BOTTOM_UP_L")
    new_line = sp.LineString([(4, 2), (4, 1)])
    lines = [
        sp.LineString([j.as_tuple for j in i.as_list]) for i in dom.paired_coords
    ] + [new_line]
    # print(lines)
    mlines = sp.MultiLineString(lines)

    # plot_line(mlines)
    # plt.show()

    print(list(dom.paired_coords))
    nc_0 = PairedCoord(Coord(2, 2), Coord(4, 2))
    nc_1 = PairedCoord(Coord(4, 2), Coord(4, 1))
    nc_2 = PairedCoord(Coord(4, 1), Coord(2, 1))
    ncs = [nc_0, nc_1, nc_2]
    new_coords = [i for i in dom.paired_coords[0:4]] + ncs + [dom.paired_coords[-1]]
    print(new_coords)

    coords = [i.last for i in new_coords]
    dom2 = FancyOrthoDomain(coords)
    pol2 = dom2.polygon

    res = sp.make_valid(pol2, method="structure")
    print(res)

    # fig, ax = plt.subplots()
    # plot_polygon(dom2.shapely_polygon)
    # plt.show()

    fig, ax = plt.subplots()
    plot_polygon(res)
    plt.show()


if __name__ == "__main__":
    test_recreating_geom()
