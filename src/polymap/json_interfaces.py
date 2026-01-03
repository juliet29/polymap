from pathlib import Path
from pydantic import TypeAdapter
from polymap.geometry.ortho import FancyOrthoDomain
from polymap.interfaces import CoordsType
from utils4plans.io import read_json

from polymap.layout.interfaces import Layout


layout_type_adapter = TypeAdapter(dict[str, CoordsType])


def read_layout_from_path(path: Path):
    res = read_json(path)
    layout_input = layout_type_adapter.validate_python(res)
    domains: list[FancyOrthoDomain] = []
    for k, v in layout_input.items():
        domain = FancyOrthoDomain.from_tuple_list(v)
        domain.set_name(k)
        domains.append(domain)

    return Layout(domains)
