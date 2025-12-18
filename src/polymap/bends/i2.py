import geom

import networkx as nx
from dataclasses import dataclass, field

from rich.pretty import pretty_repr
from utils4plans.lists import chain_flatten
from polymap.bends.graph import get_predecesor, get_successor
from polymap.geometry.modify.update import Move
from polymap.geometry.ortho import FancyOrthoDomain
from polymap.geometry.surfaces import Surface
from rich import print


def get_nonzero_component(v: geom.Vector):
    res = list(filter(lambda x: x != 0, [v.x, v.y]))
    assert len(res) == 1, f"Invalid v. Possibly non-ortho: {v}"
    return res[0]


def make_surface_rep(surface: Surface):
    return f"{surface.name} |  {str(surface.coords)}"


@dataclass
class Bend:
    @property
    def surfaces(self) -> list[Surface]:
        return [v for v in self.__dict__.values() if isinstance(v, Surface)]

    @property
    def surface_names(self):
        return [i.name for i in self.surfaces]

    @property
    def surface_tuple(self):
        return tuple(self.surfaces)

    def __str__(self):
        return f"{type(self)}({self.surface_names})"

    def __rich_repr__(self):
        for k, v in self.__dict__.items():
            if isinstance(v, Surface):
                yield k, make_surface_rep(v)


@dataclass
class PiOne(Bend):
    a: Surface
    s1: Surface
    b: Surface
    domain: FancyOrthoDomain

    @classmethod
    def from_surfaces(cls, domain: FancyOrthoDomain, G: nx.DiGraph, s1: Surface):
        a = get_predecesor(G, s1.name)
        b = get_successor(G, s1.name)
        return cls(a, s1, b, domain)

    @property
    def are_vectors_correct(self):
        exp = self.a.direction_vector == -self.b.direction_vector
        return exp

    @property
    def get_move(self):
        # TODO fix!
        m = Move(self.domain, self.a, get_nonzero_component(self.s1.vector))
        return [m]


@dataclass
class PiTwo(Bend):
    a: Surface
    s1: Surface
    b: Surface
    s2: Surface
    c: Surface
    domain: FancyOrthoDomain

    @classmethod
    def from_surfaces(
        cls, domain: FancyOrthoDomain, G: nx.DiGraph, s1: Surface, s2: Surface
    ):
        a = get_predecesor(G, s1.name)
        b = get_successor(G, s1.name)
        c = get_successor(G, s2.name)
        return cls(a, s1, b, s2, c, domain)

    @property
    def are_vectors_correct(self):
        exp1 = self.s1.direction_vector == -self.s2.direction_vector
        exp2 = (
            self.a.direction_vector
            == self.b.direction_vector
            == self.c.direction_vector
        )
        return exp1 and exp2

    @property
    def get_move(self):
        # TODO fix!
        m = Move(self.domain, self.a, get_nonzero_component(self.s1.vector))
        return [m]


@dataclass
class PiThree(Bend):
    a: Surface
    s1: Surface
    s2: Surface
    s3: Surface
    b: Surface
    domain: FancyOrthoDomain

    @classmethod
    def from_surfaces(
        cls,
        domain: FancyOrthoDomain,
        G: nx.DiGraph,
        s1: Surface,
        s2: Surface,
        s3: Surface,
    ):
        a = get_predecesor(G, s1.name)
        b = get_successor(G, s3.name)
        return cls(a, s1, s2, s3, b, domain)

    @property
    def are_vectors_correct(self):
        exp1 = self.s1.direction_vector == -self.s3.direction_vector
        exp2 = (
            self.a.direction_vector
            == self.b.direction_vector
            == self.s2.direction_vector
        )
        return exp1 and exp2

    @property
    def get_move(self):
        # TODO fix!
        m = Move(self.domain, self.a, get_nonzero_component(self.s1.vector))
        return [m]


@dataclass
class KappaOne(Bend):
    a: Surface
    s1: Surface
    b: Surface
    domain: FancyOrthoDomain

    @classmethod
    def from_surfaces(cls, domain: FancyOrthoDomain, G: nx.DiGraph, s1: Surface):
        a = get_predecesor(G, s1.name)
        b = get_successor(G, s1.name)
        return cls(a, s1, b, domain)

    @property
    def are_vectors_correct(self):
        exp = (self.a.direction_vector == self.b.direction_vector) and (
            self.s1.parallel_axis != self.a.parallel_axis
        )
        return exp

    @property
    def get_move(self):
        m = Move(self.domain, self.a, get_nonzero_component(self.s1.vector))
        return [m]


@dataclass
class KappaTwo(Bend):
    a: Surface
    s1: Surface
    s2: Surface
    b: Surface
    domain: FancyOrthoDomain

    @classmethod
    def from_surfaces(
        cls, domain: FancyOrthoDomain, G: nx.DiGraph, s1: Surface, s2: Surface
    ):
        a = get_predecesor(G, s1.name)
        b = get_successor(G, s2.name)
        return cls(a, s1, s2, b, domain)

    @property
    def are_vectors_correct(self):
        v1 = self.a.direction_vector
        v2 = self.s1.direction_vector

        exp1 = v1 == self.s2.direction_vector
        exp2 = v2 == self.b.direction_vector

        return exp1 and exp2

    @property
    def get_move(self):
        if self.s1.direction_vector == self.b.direction_vector:
            m1 = Move(self.domain, self.s1, get_nonzero_component(self.s2.vector))
        else:
            m1 = Move(self.domain, self.s2, get_nonzero_component(self.s1.vector))
        return [m1]


class ProblemIdentifyingBend(Exception):
    def __init__(self, reason: str, bends: list[Bend]) -> None:
        self.reason = reason
        self.bends = bends


@dataclass
class BendHolder:
    pi2s: list[PiTwo] = field(default_factory=list)
    pi3s: list[PiThree] = field(default_factory=list)
    kappa2s: list[KappaTwo] = field(default_factory=list)
    pis: list[PiOne] = field(default_factory=list)
    kappas: list[KappaOne] = field(default_factory=list)
    large: list[list[str]] = field(default_factory=list)
    not_found: list[list[str]] = field(default_factory=list)

    @property
    def summary(self):
        sdata = {}
        for name, val in self.__dict__.items():
            sdata[name] = len(val)
        return f"BendHolder: {pretty_repr(sdata)}"

    def get_next_bend(self):
        if self.pi2s:
            res = self.pi2s[0]
        elif self.pi3s:
            res = self.pi3s[0]
        elif self.kappa2s:
            res = self.kappa2s[0]
        elif self.pis:
            res = self.pis[0]
        elif self.kappas:
            res = self.kappas[0]
        else:
            raise ProblemIdentifyingBend(
                "Bend holder is empty!",
                chain_flatten([v for v in self.__dict__.values()]),
            )

        print(f"Next bend is {str(res)}")
        return res
