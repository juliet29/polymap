import geom
from dataclasses import dataclass, field

from utils4plans.lists import chain_flatten
from polymap.geometry.modify.update import Move
from polymap.geometry.ortho import FancyOrthoDomain
from polymap.geometry.surfaces import Surface
from rich import print


def get_nonzero_component(v: geom.Vector):
    # todo should check is orto ..
    res = list(filter(lambda x: x != 0, [v.x, v.y]))
    assert len(res) == 1, f"Invalid v. Possibly non-ortho: {v}"
    return res[0]


def make_surface_rep(surface: Surface):
    return f"{surface.name_w_domain} |  {str(surface.coords)}"


@dataclass
class Bend:
    @property
    def surfaces(self):
        return []

    @property
    def surface_names(self):
        return []

    def __str__(self):
        return f"{type(self)}({self.surface_names})"


@dataclass
class EtaBend(Bend):
    a: Surface
    s1: Surface
    b: Surface
    domain: FancyOrthoDomain

    def __rich_repr__(self):
        yield "a", make_surface_rep(self.a)
        yield "s1", make_surface_rep(self.s1)
        yield "b", make_surface_rep(self.b)

    @property
    def surfaces(self):
        return [self.a, self.s1, self.b]

    @property
    def surface_names(self):
        return [i.name_w_domain for i in self.surfaces]

    @property
    def surface_tuple(self):
        return (self.a, self.s1, self.b)


@dataclass
class ZetaBend(EtaBend):
    @classmethod
    def from_eta(cls, e: EtaBend):
        return cls(*e.surface_tuple, e.domain)

    @property
    def get_move(self):
        m = Move(self.domain, self.a, get_nonzero_component(self.s1.vector))

        return [m]


@dataclass
class BetaBend(EtaBend):

    @classmethod
    def from_eta(cls, e: EtaBend):
        return cls(*e.surface_tuple, e.domain)

    @property
    def get_move(self):
        m = Move(self.domain, self.s1, get_nonzero_component(self.b.vector))

        return [m]


@dataclass
class PiBend(Bend):
    a: Surface
    s1: Surface
    b: Surface
    s2: Surface
    c: Surface
    domain: FancyOrthoDomain

    def __rich_repr__(self):
        yield "a", make_surface_rep(self.a)
        yield "s1", make_surface_rep(self.s1)
        yield "b", make_surface_rep(self.b)
        yield "s2", make_surface_rep(self.s2)
        yield "c", make_surface_rep(self.c)

    @property
    def surfaces(self):
        return [self.a, self.s1, self.b, self.s2, self.c]

    @property
    def surface_names(self):
        return [i.name_w_domain for i in self.surfaces]

    @property
    def get_move(self):
        m = Move(self.domain, self.b, -1 * get_nonzero_component(self.s1.vector))
        return [m]


@dataclass
class KappaBend(Bend):
    a: Surface
    s1: Surface
    s2: Surface
    b: Surface
    domain: FancyOrthoDomain

    def __rich_repr__(self):
        yield "a", make_surface_rep(self.a)
        yield "s1", make_surface_rep(self.s1)
        yield "s2", make_surface_rep(self.s2)
        yield "b", make_surface_rep(self.b)

    @property
    def surfaces(self):
        return [self.a, self.s1, self.s2, self.b]

    @property
    def surface_names(self):
        return [i.name_w_domain for i in self.surfaces]

    @property
    def get_move(self):
        m1 = Move(self.domain, self.s1, get_nonzero_component(self.s2.vector))

        m2 = Move(self.domain, self.s2, get_nonzero_component(self.s1.vector))
        return [m1, m2]  # [m1, m2]


@dataclass
class GammaBend(Bend):
    s1: Surface
    s2: Surface
    s3: Surface
    domain: FancyOrthoDomain

    def __rich_repr__(self):
        yield "s1", make_surface_rep(self.s1)
        yield "s2", make_surface_rep(self.s2)
        yield "s3", make_surface_rep(self.s3)

    @property
    def surfaces(self):
        return [self.s1, self.s2, self.s3]

    @property
    def surface_names(self):
        return [i.name_w_domain for i in self.surfaces]

    @property
    def get_move(self):
        m1 = Move(self.domain, self.s2, get_nonzero_component(self.s3.vector))
        return [m1]


class ProblemIdentifyingBend(Exception):
    def __init__(self, reason: str, bends: list[Bend]) -> None:
        self.reason = reason
        self.bends = bends


@dataclass
class BendHolder:
    etas: list[EtaBend] = field(default_factory=list)
    zetas: list[ZetaBend] = field(default_factory=list)
    betas: list[BetaBend] = field(default_factory=list)
    pis: list[PiBend] = field(default_factory=list)
    kappas: list[KappaBend] = field(default_factory=list)
    gammas: list[GammaBend] = field(default_factory=list)

    def summarize(self):
        sdata = {}
        for name, val in self.__dict__.items():
            sdata[name] = len(val)
        print(f"BendHolder: {sdata}")

    def get_next_bend(self):
        if self.gammas:
            res = self.gammas[0]
        elif self.betas:
            res = self.betas[0]
        elif self.kappas:
            res = self.kappas[0]
        elif self.pis:
            res = self.pis[0]
        elif self.zetas:
            res = self.zetas[0]
        else:
            raise ProblemIdentifyingBend(
                "Bend holder is empty!",
                chain_flatten(
                    [self.gammas, self.kappas, self.pis, self.betas, self.zetas]
                ),
            )

        print(f"Next bend is {str(res)}")
        return res
