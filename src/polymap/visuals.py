import shapely as sp
from shapely import plotting
import matplotlib.pyplot as plt
from polymap.examples.sample_domains import create_ortho_domain
from matplotlib.axes import Axes


def plot_polygon(p: sp.Polygon | sp.MultiPolygon, ax: Axes | None = None ):
    if not ax: 
        fig, ax = plt.subplots()
    plotting.plot_polygon(p, ax=ax)
    if not ax: 
        plt.show()


def plot_line(p: sp.LineString | sp.MultiLineString):
    fig, ax = plt.subplots()
    plotting.plot_line(p, ax=ax)
    plt.show()


if __name__ == "__main__":
    dom = create_ortho_domain("NON_ORTHO")
    plot_polygon(dom.shapely_polygon)
