from polymap.geometry.ortho import FancyOrthoDomain, find_and_replace_in_list
from polymap.geometry.surfaces import Surface
from polymap.interfaces import CoordsType
from polymap.visuals import plot_polygon


import shapely as sp
from utils4plans.lists import chain_flatten, get_unique_one
from utils4plans.sets import set_difference
from utils4plans.io import read_json
from pathlib import Path
from polymap.paths import MSD_PATHS
from typing import TypeVar


from dataclasses import dataclass

T = TypeVar("T")


# # TODO add to utils4plans
# def set_update(existing: list[T], new: list[T]):
#     diff = set_difference(existing, new)
#     return list(set(diff).union(set(new)))


@dataclass
class Layout:
    domains: list[FancyOrthoDomain]
    # post init -> assert names are unique!

    def plot_layout(self):
        polygons = sp.MultiPolygon([i.polygon for i in self.domains])
        plot_polygon(polygons)

    def get_domain(self, name):
        return get_unique_one(self.domains, lambda x: x.name == name)

    @property
    def surfaces(self):
        return chain_flatten([i.surfaces for i in self.domains])

    def get_other_surfaces(self, surf: Surface):
        return set_difference(self.surfaces, [surf])

    def get_surface_by_name(self, surf_name: str):
        return get_unique_one(self.surfaces, lambda x: str(x) == surf_name)

    def update_layout(self, new_domains: list[FancyOrthoDomain]):
        domains_to_replace = [self.get_domain(i.name) for i in new_domains]
        updated_domains = find_and_replace_in_list(
            self.domains, domains_to_replace, new_domains
        )
        return Layout(updated_domains)
        # updated_domains = set_update(self.domains, new_domains)
        # return Layout(updated_domains)


def create_layout_from_dict(
    layout: dict[str, CoordsType],
):  # TODO: CoordsType is a misnomer
    domains: list[FancyOrthoDomain] = []
    for k, v in layout.items():
        domain = FancyOrthoDomain.from_tuple_list(v)
        domain.set_name(k)
        domains.append(domain)

    return Layout(domains)


def create_layout_from_json(file_name: str, folder_path: Path = MSD_PATHS):
    data: dict[str, CoordsType] = read_json(folder_path, file_name)
    domains: list[FancyOrthoDomain] = []
    for k, v in data.items():
        domain = FancyOrthoDomain.from_tuple_list(v)
        domain.set_name(k)
        domains.append(domain)

    return Layout(domains)
