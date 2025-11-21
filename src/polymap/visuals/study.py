import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from polymap.process.interfaces import ProcessGraphPairs, ProcessLayouts
from polymap.visuals.visuals import plot_graph_pairs_and_layout, plot_layout
from polymap.paths import DynamicPaths


def save_figure(layout_id: str, fig: Figure):
    fig.set_layout_engine("constrained")
    fig.savefig(
        fname=DynamicPaths.process_figs / f"{layout_id}.pdf", format="pdf", dpi=500
    )


def make_study_plot(pl: ProcessLayouts, pgp: ProcessGraphPairs):
    ALPHA = 0.7
    fig, axs = plt.subplots(ncols=2, nrows=3)

    ax0, ax1, ax2, ax3, ax4, ax5 = axs.flatten()

    plot_layout(pl.original, str(pl.id), ax0, show=False)
    plot_layout(pl.simplified, "simplified", ax1, show=False)

    plot_graph_pairs_and_layout(pl.simplified, "xgraph", pgp.x, ax2, alpha=ALPHA)
    plot_layout(pl.xpull, "xpull", ax3, show=False)

    plot_graph_pairs_and_layout(pl.xpull, "ygraph", pgp.y, ax4, alpha=ALPHA)
    plot_layout(pl.ypull, "ypull", ax5, show=False)

    save_figure(pl.id, fig)

    # plt.show()

    # later, save in folder for layout, along with a log file..
