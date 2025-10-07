import shapely as sp
from shapely import plotting
import matplotlib.pyplot as plt


def plot_polygon(p: sp.Polygon | sp.MultiPolygon):
    fig, ax = plt.subplots()
    plotting.plot_polygon(p, ax=ax)
    plt.show()
