from typing import Literal
from polymap.paths import static_paths
from polymap.layout.interfaces import create_layout_from_json

from polymap.paths import DynamicPaths

MSD_IDs = Literal[
    "106493",
    "146903",
    "146915",
    "146965",
    "19792",
    "22940",
    "27540",
    "48204",
    "48205",
    "49943",
    "56958",
    "57231",
    "58613",
    "60529",
    "60532",
    "60553",
    "67372",
    "67408",
    "71308",
    "71318",
]


def get_msd_plan():
    filename = "oneoff/layout"
    res = create_layout_from_json(filename, static_paths.inputs)
    print(res)
    return res


def get_all_msd_layouts():
    source_path = DynamicPaths.MSD_PATHS
    paths = sorted([i for i in source_path.iterdir()])
    layouts = {
        path.stem: create_layout_from_json(path.stem, source_path) for path in paths
    }
    return layouts


def get_one_msd_layout(id: MSD_IDs | None = None):
    source_path = DynamicPaths.MSD_PATHS

    stems = sorted([i.stem for i in source_path.iterdir()])

    if id:
        stem = id
        assert stem in stems
    else:
        stem = stems[0]

    return stem, create_layout_from_json(stem, source_path)


if __name__ == "__main__":
    get_msd_plan()
