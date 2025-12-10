import geom
from dataclasses import dataclass, field
from polymap.geometry.modify.update import Move
from polymap.geometry.modify.delete import Delete
from polymap.geometry.ortho import FancyOrthoDomain
from polymap.geometry.surfaces import Surface


def get_nonzero_component(v: geom.Vector):
    # todo should check is orto ..
    res = list(filter(lambda x: x != 0, [v.x, v.y]))
    assert len(res) == 1, f"Invalid v. Possibly non-ortho: {v}"
    return res[0]


def make_surface_rep(surface: Surface):
    return f"{surface.name} |  {str(surface.coords)}"


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

    # @property
    # def first(self):
    #     return self.surfaces[0]


@dataclass
class ZetaBend(Bend):
    a: Surface
    s1: Surface
    b: Surface
    domain: FancyOrthoDomain

    def __rich_repr__(self):
        yield "a", self.a
        yield "s1", self.s1
        yield "b", self.b

    @property
    def surfaces(self):
        return [self.a, self.s1, self.b]

    @property
    def surface_names(self):
        return [i.name for i in self.surfaces]

    @property
    def surface_tuple(self):
        return (self.a, self.s1, self.b)

    @property
    def get_move(self):
        return Move(
            self.domain, self.a, get_nonzero_component(self.s1.vector)
        )  # TODO: this should really be get value, for the case of vertical bend..


@dataclass
class PiBend(Bend):
    a: Surface
    s1: Surface
    b: Surface
    s2: Surface
    c: Surface
    domain: FancyOrthoDomain

    def __rich_repr__(self):
        yield "a", self.a
        yield "s1", self.s1
        yield "b", self.b
        yield "s2", self.s2
        yield "c", self.c

    @property
    def surfaces(self):
        return [self.a, self.s1, self.b, self.s2, self.c]

    @property
    def surface_names(self):
        return [i.name for i in self.surfaces]

    @property
    def get_move(self):
        return Move(self.domain, self.b, -1 * get_nonzero_component(self.s1.vector))


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
        return [i.name for i in self.surfaces]

    @property
    def get_move(self):
        m = Move(self.domain, self.s1, get_nonzero_component(self.s2.vector))
        d = Delete(self.domain.paired_coords, self.s2.coords)
        return m


@dataclass
class EtaBend(Bend):
    s1: Surface
    s2: Surface
    s3: Surface


@dataclass
class BendHolder:
    zetas: list[ZetaBend] = field(default_factory=list)
    pis: list[PiBend] = field(default_factory=list)
    kappas: list[KappaBend] = field(default_factory=list)
    etas: list[EtaBend] = field(default_factory=list)

    def summarize(self):
        for name, val in self.__dict__.items():
            print(f"{name}: {len(val)}")

    def get_next_bend(self):
        if self.kappas:
            res = self.kappas[0]
        elif self.pis:
            res = self.pis[0]
        elif self.zetas:
            res = self.zetas[0]
        else:
            raise Exception("Bend holder is empty!")

        print(f"Next bend is {str(res)}")
        return res
