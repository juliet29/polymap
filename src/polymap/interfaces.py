from typing import Any, Generator, Callable


GraphPairs = dict[str, list[str]]
CoordsTypeJSON = list[list[float]]


def make_repr(fx: Callable[[], Generator[tuple[str, Any]]], obj: object | str):
    repr_str: list[str] = []
    append = repr_str.append
    inp = fx()
    for arg in inp:
        key, value = arg
        append(f"{key}={value}")
    if isinstance(obj, str):
        return f"{obj}({'\n '.join(repr_str)})"
    else:
        return f"{obj.__class__.__name__}({', '.join(repr_str)})"


def make_repr_obj(fx: Callable[[], Generator[tuple[str, Any]]]):
    inp = fx()
    d = {}
    for arg in inp:
        key, value = arg
        d[key] = value
    return d
    # if isinstance(obj, str):
    #     return f"{obj}({'\n '.join(repr_str)})"
    # else:
    #     return f"{obj.__class__.__name__}({', '.join(repr_str)})"
