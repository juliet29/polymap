from polymap.examples.msd import MSD_IDs, get_one_msd_layout
from polymap.process.process import process_layout
from typing import get_args
from rich import print


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
            fin_id = process_layout(id)
        except Exception as e:
            print(e)
            continue
        good_ids.append(fin_id)

        print(f"[bold pink] GOOD IDS: {good_ids} ------------------- [/bold pink]")

    print(good_ids)


def count_domains():
    len_doms = 0
    for id in get_args(MSD_IDs):
        id, layout = get_one_msd_layout(id)
        lend = len(layout.domains)
        len_doms += lend
    print(len_doms)


if __name__ == "__main__":
    count_domains()
    # for id in GOOD_IDS:
    #     fin_id = process_layout(id)
