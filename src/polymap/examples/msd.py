from polymap.paths import static_paths
from polymap.layout.interfaces import create_layout_from_json

from polymap.paths import DynamicPaths
from random import seed

seed(1234567)


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


def get_one_msd_layout(id: int | None = None):
    source_path = DynamicPaths.MSD_PATHS

    stems = sorted([i.stem for i in source_path.iterdir()])

    if id:
        stem = str(id)
        assert stem in stems
    else:
        stem = stems[0]

    return stem, create_layout_from_json(stem, source_path)


if __name__ == "__main__":
    get_msd_plan()
