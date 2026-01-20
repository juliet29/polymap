from polymap.json_interfaces import read_layout_from_path
from polymap.paths import DynamicPaths


def test_read_layout():
    path = DynamicPaths.MSD_PATHS / "106493.json"
    read_layout_from_path(path)


# TODO: replace with trials / pydantic
# def test_dump_layout():
#     path = DynamicPaths.MSD_PATHS / "106493.json"
#     layout = read_layout_from_path(path)
#     print(layout.dump())
#
#
# def test_read_after_dump():
#     path = static_paths.temp / "msd/19792/rotate/out.json"
#     layout = read_layout_from_path(path)
#     print(layout.dump())
#

if __name__ == "__main__":
    pass
