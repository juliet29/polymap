from utils4plans.io import read_json
from polymap.paths import static_paths
import shapely as sp
from polymap.layout.interfaces import create_layout_from_json


def get_msd_plan():
    filename = "oneoff/layout"
    res = create_layout_from_json(filename, static_paths.inputs)
    print(res)
    return res


if __name__ == "__main__":
    get_msd_plan()
