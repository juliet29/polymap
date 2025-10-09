from polymap.geometry.ortho import FancyOrthoDomain
from polymap.geometry.surfaces import Surface
from polymap.interfaces import CoordsType
from polymap.visuals import plot_polygon


import shapely as sp
from utils4plans.lists import chain_flatten, get_unique_one
from utils4plans.sets import set_difference


from dataclasses import dataclass


@dataclass
class Layout:
    domains: list[FancyOrthoDomain]
    # post init -> assert names are unique!

    def plot_layout(self):
        polygons = sp.MultiPolygon([i.shapely_polygon for i in self.domains])
        plot_polygon(polygons)

    def get_domain(self, name):
        return get_unique_one(self.domains, lambda x: x.name == name)

    @property
    def surfaces(self):
        return chain_flatten([i.surfaces for i in self.domains])

    def get_other_surfaces(self, surf: Surface):
        return set_difference(self.surfaces, [surf])
    
    def get_surface_by_name(self, surf_name:str):
        return get_unique_one(self.surfaces, lambda x: str(x) == surf_name)


def create_layout_from_dict(
    layout: dict[str, CoordsType],
):  # TODO: CoordsType is a misnomer
    domains: list[FancyOrthoDomain] = []
    for k, v in layout.items():
        domain = FancyOrthoDomain.from_tuple_list(v)
        domain.set_name(k)
        domains.append(domain)

    return Layout(domains)
