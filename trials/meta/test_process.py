from loguru import logger
from polymap import logconf
from polymap.examples.msd import MSD_IDs, get_one_msd_layout
from polymap.process.process import process_layout
from typing import get_args
from rich import print

from polymap.visuals.visuals import plot_layout


# GOOD_IDS = ["106493", "146915", "56958", "57231", "60553", "71308", "71318"]
GOOD_IDS: list[MSD_IDs] = [
    # # "146903", # bad
    # "146915",
    # "146965",
    # "19792",
    # # "48204",# bad
    # "48205", # bad
    # "56958",
    # "57231",
    # "60529",
    # "60553",
    # "67372",  # failed -> cannot norm 0 vector after x
    # "67408", # same issue
    "71308",
    "71318",
]


def run_whole_process():
    ids = get_args(MSD_IDs)
    good_ids = []
    for id in ids:
        try:
            logger.log("START", f"studying {id}")
            fin_layout = process_layout(id)
            plot_layout(fin_layout, layout_name=id)

        except Exception as e:
            print(e)
            continue
        good_ids.append(id)

        logger.log("END", f"finished studying {id}\n")

    logger.log(
        "SUMMARY", f"[bold pink] GOOD IDS: {good_ids} ------------------- [/bold pink]"
    )


def count_domains():
    len_doms = 0
    for id in get_args(MSD_IDs):
        id, layout = get_one_msd_layout(id)
        lend = len(layout.domains)
        len_doms += lend
    print(len_doms)


if __name__ == "__main__":
    logconf.logset()
    run_whole_process()
    # for id in GOOD_IDS:
    #     fin_id = process_layout(id)
