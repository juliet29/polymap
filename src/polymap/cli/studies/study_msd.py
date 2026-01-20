from collections import Counter
from typing import NamedTuple, get_args

from loguru import logger
from rich.pretty import pretty_repr
from utils4plans import logconfig
from polymap.bends.bends import assign_bends
from polymap.bends.interfaces import Bend, BendListSummary, BendNames, DomainSummary
from polymap.bends.main import (
    DomainCleanIterationFailure,
    remove_bends_from_layout,
    remove_all_bends_from_domain,
)
from polymap.examples.msd import (
    MSDDomain,
    MSDDomainName,
    get_all_msd_domains,
    get_msd_layouts_as_objects,
)
from polymap.bends.utils import make_repr
from polymap.visuals.visuals import plot_domain_with_surfaces, plot_layout_comparison


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

    @property
    def data(self):
        return list(
            map(
                lambda x: DomainRes(
                    x, assign_bends(x.domain, x.name.display_name).summary
                ),
                self.doms,
            )
        )

    def report(self):
        summary = summarize_across_domains(self.data)
        logger.info(pretty_repr(summary))

    def study_failing_bends(self, type_: BendNames):
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
            plot_domain_with_surfaces(dom.domain, title=dom.name.display_name)

    def study_moves_one_domain(self):
        dom = self.doms[0]
        remove_all_bends_from_domain(dom)

    def study_moves_all_domain(self):
        def handle(dom: MSDDomain):
            try:
                remove_all_bends_from_domain(dom, show_failure=False)
            except DomainCleanIterationFailure as e:
                failures.append((e.domain, e.fail_type))
                fail_counter[e.fail_type] += 1
                if e.fail_type == "Invalid Move":
                    assert isinstance(e.current_bend, Bend)
                    fail_bend_counter[e.current_bend.bend_name] += 1
                return

            successes.append(dom.name.display_name)

        def report():
            s = f"[green]PASS:{len(successes)}/{dom_counter}"
            f = f"[red]FAIL:{len(failures)}/{dom_counter}"

            # TODO: need a logure log that is more like a summary...
            logger.success(f"SUMMARY:{s} | {f}")
            logger.success(fail_counter)
            logger.success(fail_bend_counter)

        failures = []
        fail_counter = Counter()
        fail_bend_counter = Counter()
        successes = []
        dom_counter = 0

        for dom in self.doms:
            handle(dom)
            dom_counter += 1

        report()


class StudyMSDLayouts:
    layouts = get_msd_layouts_as_objects()

    def study_all(self, show_success: bool = False, lim: int | None = None):
        tracker = {}

        if lim:
            layouts = self.layouts[0:lim]
        else:
            layouts = self.layouts

        for group in layouts:
            new_layout, bad_domains = remove_bends_from_layout(
                group.layout, group.layout_id
            )
            tracker[group.layout_id] = bad_domains
            if show_success:
                plot_layout_comparison(
                    [group.layout, new_layout], [group.layout_id, "bends cleaned"]
                )

        logger.success(tracker)


if __name__ == "__main__":
    logconfig.logset(debug_level="SUCCESS")
    # s = StudyMSDBends()
    # s.study_moves_all_domain()
    # s.summarize_failing("pi3s")

    s = StudyMSDLayouts()
    s.study_all(lim=2)
