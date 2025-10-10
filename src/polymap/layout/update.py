from polymap.layout.interfaces import Layout
from polymap.layout.graph import create_graph_for_layout
import networkx as nx


def update_layout_by_axis(layout: Layout, G: nx.DiGraph):
    pass


def update_layout(layout: Layout):
    Gx, Gy = create_graph_for_layout(layout)
