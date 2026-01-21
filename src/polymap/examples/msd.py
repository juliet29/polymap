from typing import Literal, get_args
from typing_extensions import NamedTuple
from utils4plans.lists import chain_flatten
from polymap.geometry.ortho import FancyOrthoDomain
from polymap.paths import static_paths
from polymap.geometry.layout import Layout, create_layout_from_json

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

DEFAULT_MSD: MSD_IDs = "106493"


class MSDLayout(NamedTuple):
    layout_id: str | MSD_IDs
    layout: Layout


class MSDDomainName(NamedTuple):
    layout_id: str | MSD_IDs
    domain_name: str

    def __repr__(self) -> str:
        return f"({self.layout_id}, {self.domain_name})"

    @property
    def display_name(self):
        return self.__repr__()


class MSDDomain(NamedTuple):
    name: MSDDomainName
    domain: FancyOrthoDomain


def get_oneoff_msd_plan():
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
        stem = DEFAULT_MSD
        assert stem in stems

    return stem, create_layout_from_json(stem, source_path)


def get_msd_layouts_as_objects():
    return [MSDLayout(*get_one_msd_layout(id)) for id in get_args(MSD_IDs)]


def get_all_msd_domains():
    def get_layout_domains(msd_id: str, layout: Layout):
        m: MSD_IDs = msd_id  # pyright: ignore[reportAssignmentType]
        return [MSDDomain(MSDDomainName(m, d.name), d) for d in layout.domains]

    all_layouts = [get_one_msd_layout(id) for id in get_args(MSD_IDs)]
    doms = [get_layout_domains(id, layout) for id, layout in all_layouts]
    return chain_flatten(doms)


if __name__ == "__main__":
    get_oneoff_msd_plan()
