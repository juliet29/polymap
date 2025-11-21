from polymap.examples.msd import MSD_IDs
from polymap.process.process import process_layout
from typing import get_args
from rich import print


if __name__ == "__main__":
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
