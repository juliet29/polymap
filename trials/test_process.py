from polymap.examples.msd import MSD_IDs
from polymap.process.process import process_layout
from typing import get_args
from rich import print


GOOD_IDS = ["106493", "146915", "56958", "57231", "60553", "71308", "71318"]


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


if __name__ == "__main__":
    for id in GOOD_IDS:
        fin_id = process_layout(id)
