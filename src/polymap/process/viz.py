import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from polymap.process.interfaces import ProcessGraphPairs, ProcessLayouts
from polymap.visuals.visuals import plot_graph_pairs_and_layout, plot_layout
from polymap.paths import static_paths
from utils4plans.io import get_or_make_folder_path


SAVE_FOLDER = "process_figs2"


def save_figure(layout_id: str, fig: Figure, folder_name: str = SAVE_FOLDER):
    fig.set_layout_engine("constrained")
    path = get_or_make_folder_path(static_paths.temp, folder_name)
    fig.savefig(fname=path / f"{layout_id}.png", format="png", dpi=500)


def make_study_plot(pl: ProcessLayouts, pgp: ProcessGraphPairs):
    ALPHA = 0.7
    fig, axs = plt.subplots(ncols=2, nrows=2, sharex=True, sharey=True)

    ax2, ax3, ax4, ax5 = axs.flatten()

    # plot_layout(pl.original, str(pl.id), ax0, show=False)
    # plot_layout(pl.simplified, "simplified", ax1, show=False)

    plot_graph_pairs_and_layout(
        pl.simplified, "xgraph", pgp.x, ax2, alpha=ALPHA, add_labels=True
    )
    plot_layout(pl.xpull, "xpull", ax3, show=False, add_labels=False)

    plot_graph_pairs_and_layout(
        pl.xpull, "ygraph", pgp.y, ax4, alpha=ALPHA, add_labels=False
    )
    plot_layout(pl.ypull, "ypull", ax5, add_labels=False, show=False)

    fig.suptitle(pl.id)

    # save_figure(pl.id, fig)

    plt.show()

    # later, save in folder for layout, along with a log file..
