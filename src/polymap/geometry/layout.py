from polymap.geometry.ortho import FancyOrthoDomain
from polymap.geometry.surfaces import Surface
from utils4plans.geom import CoordsType


from utils4plans.lists import chain_flatten, get_unique_one
from utils4plans.sets import set_difference
from utils4plans.io import read_json
from pathlib import Path
from polymap.paths import DynamicPaths
from typing import TypeVar
from rich import print


from dataclasses import dataclass

T = TypeVar("T")


@dataclass
class Layout:
    domains: list[FancyOrthoDomain]

    def get_domain(self, name):
        return get_unique_one(self.domains, lambda x: x.name == name)

    def get_surfaces(self, substantial_only=False):
        if substantial_only:
            return chain_flatten([i.substantial_surfaces for i in self.domains])
        return chain_flatten([i.surfaces for i in self.domains])

    def get_other_surfaces(self, surf: Surface, substantial_only: bool = False):
        return set_difference(self.get_surfaces(substantial_only), [surf])

    def get_surface_by_name(self, surf_name: str):
        return get_unique_one(self.get_surfaces(), lambda x: str(x) == surf_name)

    @property
    def surface_summary(self):
        for d in self.domains:
            d.summarize_surfaces
            print("\n")

    @property
    def domain_names(self):
        print([i.name for i in self.domains])


def create_layout_from_dict(
    layout: dict[str, CoordsType],
):  # TODO: CoordsType is a misnomer
    domains: list[FancyOrthoDomain] = []
    for k, v in layout.items():
        domain = FancyOrthoDomain.from_tuple_list(v)
        domain.set_name(k)
        domains.append(domain)

    return Layout(domains)


def create_layout_from_json(file_name: str, folder_path: Path = DynamicPaths.MSD_PATHS):
    data: dict[str, CoordsType] = read_json(folder_path, file_name)
    domains: list[FancyOrthoDomain] = []
    for k, v in data.items():
        domain = FancyOrthoDomain.from_tuple_list(v)
        domain.set_name(k)
        domains.append(domain)

    return Layout(domains)
