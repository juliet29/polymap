from typing import NamedTuple, get_args

from loguru import logger
from rich.pretty import pretty_repr
from polymap import logconf
from polymap.bends.b2 import assign_bends
from polymap.bends.i2 import BendListSummary, BendNames, DomainSummary
from polymap.examples.msd import MSDDomain, MSDDomainName, get_all_msd_domains
from polymap.interfaces import make_repr


class DomainRes(NamedTuple):
    domain: MSDDomain
    bend_summary: DomainSummary


class BendTypeSummary(NamedTuple):
    size: int
    n_passing: int
    n_failing: int
    domains: list[MSDDomainName]

    def __repr__(self) -> str:
        def fx():
            yield "size", self.size
            yield "n_passing", self.n_passing
            yield "n_failing", self.n_failing

        return make_repr(fx, self)


def summarize_across_domains(data: list[DomainRes]):

    def bend_type_analysis(type_: str):
        inp = [i.bend_summary for i in data]

        info: list[BendListSummary] = [i[type_] for i in inp]
        total_size = sum([i.size for i in info])
        total_passing = sum([i.n_passing for i in info])
        total_failing = sum([i.n_failing for i in info])

        doms_1 = map(
            lambda x: x.domain.name if x.bend_summary[type_].size > 0 else None, data
        )
        doms = filter(None, doms_1)
        return BendTypeSummary(total_size, total_passing, total_failing, list(doms))

    res = {}
    for type_ in get_args(BendNames):
        res[type_] = bend_type_analysis(type_)
        res["n_large"] = sum(map(lambda x: x.bend_summary["large"], data))
        res["n_not_found"] = sum(map(lambda x: x.bend_summary["not_found"], data))
    return res


def study_msd_bends():
    doms = get_all_msd_domains()
    data = map(lambda x: DomainRes(x, assign_bends(x.domain).summary), doms)
    summary = summarize_across_domains(list(data))
    logger.info(pretty_repr(summary))

    # pi3_fails = summary["kappa2s"].domains
    #
    # logger.info(pretty_repr(pi3_fails))


if __name__ == "__main__":
    logconf.logset()
    study_msd_bends()
