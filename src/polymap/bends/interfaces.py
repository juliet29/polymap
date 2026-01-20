from typing import Literal, NamedTuple, TypedDict
import geom

from loguru import logger
import networkx as nx
from dataclasses import dataclass, field

from rich.pretty import pretty_repr
from utils4plans.lists import chain_flatten
from polymap.bends.graph import get_predecesor, get_successor
from polymap.geometry.modify.update import Move
from polymap.geometry.ortho import FancyOrthoDomain
from polymap.geometry.surfaces import Surface

from polymap.bends.utils import make_repr_obj


def get_nonzero_component(v: geom.Vector):
    res = list(filter(lambda x: x != 0, [v.x, v.y]))
    assert len(res) == 1, f"Invalid v. Possibly non-ortho: {v}"
    return res[0]


def make_surface_rep(surface: Surface):
    return f"{surface.name_w_domain} | {surface.aligned_vector} | {surface.is_small} |  {str(surface.coords)} "


@dataclass
class Bend:
    @property
    def surfaces(self) -> list[Surface]:
        return [v for v in self.__dict__.values() if isinstance(v, Surface)]

    @property
    def surface_names(self):
        return [i.name_w_domain for i in self.surfaces]

    @property
    def surface_tuple(self):
        return tuple(self.surfaces)

    def expected_vectors(self, log: bool) -> tuple[bool] | tuple[bool, bool]: ...

    @property
    def are_vectors_correct(self) -> bool: ...

    @property
    def bend_name(self):
        return f"{type(self)}"

    def __str__(self):
        return f"{type(self)}({self.surface_names})"

    def __rich_repr__(self):
        for k, v in self.__dict__.items():
            if isinstance(v, Surface):
                yield k, make_surface_rep(v)

    def study_vectors(self):
        def fx():
            for k, v in self.__dict__.items():
                if isinstance(v, Surface):
                    yield k, make_surface_rep(v)

        obj = make_repr_obj(fx)
        return pretty_repr(obj)


@dataclass
class PiOne(Bend):
    a: Surface
    s1: Surface
    b: Surface
    domain: FancyOrthoDomain

    @classmethod
    def from_surfaces(cls, domain: FancyOrthoDomain, G: nx.DiGraph, s1: Surface):
        a = get_predecesor(G, s1.name_w_domain)
        b = get_successor(G, s1.name_w_domain)
        return cls(a, s1, b, domain)

    @property
    def are_vectors_correct(self):
        exp = self.a.aligned_vector == -self.b.aligned_vector
        return exp

    @property
    def get_move(self):
        # TODO fix!
        m = Move(self.domain, self.s1, get_nonzero_component(self.b.vector))
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
        a = get_predecesor(G, s1.name_w_domain)
        b = get_successor(G, s1.name_w_domain)
        c = get_successor(G, s2.name_w_domain)
        return cls(a, s1, b, s2, c, domain)

    def expected_vectors(self, log=False):
        exp1 = self.s1.aligned_vector == -self.s2.aligned_vector
        exp2 = self.a.aligned_vector == self.b.aligned_vector == self.c.aligned_vector
        if log:
            logger.debug(exp1)
            logger.debug(exp2)
            logger.debug(exp1 and exp2)
        return (exp1, exp2)

    @property
    def are_vectors_correct(self):
        exp1, exp2 = self.expected_vectors()
        return exp1 and exp2

    @property
    def get_move(self):
        # TODO fix!
        m = Move(self.domain, self.b, get_nonzero_component(self.s2.vector))
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
        a = get_predecesor(G, s1.name_w_domain)
        b = get_successor(G, s3.name_w_domain)
        return cls(a, s1, s2, s3, b, domain)

    def expected_vectors(self, log=False):
        exp1 = self.s1.direction_vector == -self.s3.direction_vector
        exp2 = self.a.aligned_vector == self.b.aligned_vector == self.s2.aligned_vector
        if log:
            logger.debug(exp1)
            logger.debug(exp2)
            logger.debug(exp1 and exp2)

        return (exp1, exp2)

    @property
    def are_vectors_correct(self):
        exp1, exp2 = self.expected_vectors()
        return exp1 and exp2

    @property
    def get_move(self):
        # TODO fix!
        m = Move(self.domain, self.s2, get_nonzero_component(self.s3.vector))
        return [m]


@dataclass
class KappaOne(Bend):
    a: Surface
    s1: Surface
    b: Surface
    domain: FancyOrthoDomain

    @classmethod
    def from_surfaces(cls, domain: FancyOrthoDomain, G: nx.DiGraph, s1: Surface):
        a = get_predecesor(G, s1.name_w_domain)
        b = get_successor(G, s1.name_w_domain)
        return cls(a, s1, b, domain)

    @property
    def are_vectors_correct(self):
        exp = (self.a.direction_vector == self.b.direction_vector) and (
            self.s1.parallel_axis != self.a.parallel_axis
        )
        return exp

    @property
    def get_move(self):
        m = Move(self.domain, self.b, -1 * get_nonzero_component(self.s1.vector))
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
        a = get_predecesor(G, s1.name_w_domain)
        b = get_successor(G, s2.name_w_domain)
        return cls(a, s1, s2, b, domain)

    @property
    def are_vectors_correct(self):
        v1 = self.a.aligned_vector
        v2 = self.s1.aligned_vector

        exp1 = (v1 == self.s2.aligned_vector) or (v1 == -1 * self.s2.aligned_vector)
        exp2 = v2 == self.b.aligned_vector or v2 == -1 * self.b.aligned_vector

        if (not exp1) or (not exp2):
            logger.debug(exp1)
            logger.debug(exp2)
            logger.debug(self.study_vectors())

        return exp1 and exp2

    @property
    def get_move(self):
        if self.s1.direction_vector == self.b.direction_vector:
            # out
            m1 = Move(self.domain, self.s1, get_nonzero_component(self.s2.vector))
        elif self.a.direction_vector == -1 * self.s2.direction_vector:
            # out
            m1 = Move(self.domain, self.s1, get_nonzero_component(self.s2.vector))
        else:
            # in
            m1 = Move(self.domain, self.s2, -1 * get_nonzero_component(self.s1.vector))
        return [m1]


class ProblemIdentifyingBend(Exception):
    def __init__(self, reason: str, bends: list[Bend]) -> None:
        self.reason = reason
        self.bends = bends


def check_vectors(bends: list[Bend]):
    passing = []
    failing = []
    for b in bends:
        if b.are_vectors_correct:
            passing.append(b)
        else:
            failing.append(b)

    return passing, failing


class BendListSummary(NamedTuple):
    size: int
    n_passing: int
    n_failing: int

    def __repr__(self) -> str:
        def fx():
            yield "size", self.size
            yield "pass", self.n_passing

        return pretty_repr(make_repr_obj(fx))


@dataclass
class BendList:
    # TODO: is this redundant?
    bends: list[Bend]

    def __post_init__(self):
        self.passing, self.failing = check_vectors(self.bends)

    @property
    def size(self):
        return len(self.bends)

    @property
    def n_passing(self):
        return len(self.passing)

    @property
    def n_failing(self):
        return len(self.failing)

    @property
    def summary(self):
        return BendListSummary(self.size, self.n_passing, self.n_failing)


class DomainSummary(TypedDict):
    pi2s: BendListSummary
    pi3s: BendListSummary
    kappa2s: BendListSummary
    pis: BendListSummary
    kappas: BendListSummary
    large: int
    not_found: int


BendNames = Literal["pis", "pi2s", "pi3s", "kappas", "kappa2s"]


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
            if name == "large" or name == "not_found":
                sdata[name] = len(val)
            else:
                bl = BendList(val)
                sdata[name] = bl.summary
        return DomainSummary(**sdata)

    @property
    def summary_str(self):
        return f"BendHolder: {pretty_repr(self.summary)}"

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
        logger.debug(self.summary_str)
        logger.debug(f"Next bend is {str(res)}")
        return res

    def get_bend_group(self, type_: BendNames):
        return self.__getattribute__(type_)
