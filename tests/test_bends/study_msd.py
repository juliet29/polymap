from typing import NamedTuple, get_args

from loguru import logger
from rich.pretty import pretty_repr
from polymap import logconf
from polymap.bends.b2 import assign_bends
from polymap.bends.i2 import BendListSummary, BendNames, DomainSummary
from polymap.examples.msd import MSDDomain, MSDDomainName, get_all_msd_domains
from polymap.interfaces import make_repr
from polymap.visuals.visuals import plot_domain_with_surfaces


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


class StudyMSDBends:
    doms = get_all_msd_domains()
    data = list(
        map(
            lambda x: DomainRes(x, assign_bends(x.domain, x.name.display_name).summary),
            doms,
        )
    )

    def report(self):
        summary = summarize_across_domains(self.data)
        logger.info(pretty_repr(summary))

    # pi3_fails = summary["kappa2s"].domains
    #
    # logger.info(pretty_repr(pi3_fails))

    def study_failing_bends(self, type_: BendNames):
        # domains of interest
        di = filter(
            lambda x: x.bend_summary[type_].size > 0
            and x.bend_summary[type_].n_failing > 0,
            self.data,
        )
        return di

    def summarize_failing(self, type_: BendNames):
        doms_of_interest = self.study_failing_bends(type_)
        for dom, summary in doms_of_interest:
            logger.info("\n")
            logger.info(f"[bold]{dom.name}")
            bh = assign_bends(dom.domain, dom.name.display_name)
            bends = bh.get_bend_group(type_)
            for b in bends:
                logger.info(b.study_vectors())
                b.expected_vectors(log=True)
            plot_domain_with_surfaces(dom.domain)


if __name__ == "__main__":
    logconf.logset()
    s = StudyMSDBends()
    s.summarize_failing("pi2s")
