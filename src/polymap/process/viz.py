import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from polymap.process.interfaces import ProcessGraphPairs, ProcessLayouts
from polymap.visuals.visuals import plot_graph_pairs_and_layout, plot_layout
from polymap.paths import static_paths
from utils4plans.io import get_or_make_folder_path
from rich import print


SAVE_FOLDER = "process_figs2"


def save_figure(layout_id: str, fig: Figure, folder_name: str = SAVE_FOLDER):
    fig.set_layout_engine("constrained")
    path = get_or_make_folder_path(static_paths.temp, folder_name)
    fig.savefig(fname=path / f"{layout_id}.png", format="png", dpi=500)


def make_study_plot(pl: ProcessLayouts, pgp: ProcessGraphPairs):
    ALPHA = 0.8

    print(f"\nresults for {pl.id}".upper())
    print("X-GRAPH: ")
    print(pgp.x)
    print("Y-GRAPH: ")
    print(pgp.y)

    fig, axs = plt.subplots(ncols=2, nrows=3, sharex=True, sharey=True)

    ax0, ax1, ax2, ax3, ax4, ax5, ax6, ax7 = axs.flatten()

    plot_layout(pl.original, str(pl.id), ax0, show=False, add_labels=True)
    plot_layout(pl.rotated, "rotated", ax1, show=False, add_labels=False)
    plot_layout(pl.ortho, "ortho", ax2, show=False, add_labels=False)
    plot_layout(pl.simplified, "simplified", ax3, show=False, add_labels=False)

    plot_graph_pairs_and_layout(
        pl.simplified, "xgraph", pgp.x, ax4, alpha=ALPHA, add_labels=False
    )
    plot_layout(pl.xpull, "xpull", ax5, show=False, add_labels=True)

    plot_graph_pairs_and_layout(
        pl.xpull, "ygraph", pgp.y, ax6, alpha=ALPHA, add_labels=False
    )
    plot_layout(pl.ypull, "ypull", ax7, add_labels=False, show=False)

    fig.suptitle(pl.id)

    # save_figure(pl.id, fig)

    plt.show()

    # later, save in folder for layout, along with a log file..
