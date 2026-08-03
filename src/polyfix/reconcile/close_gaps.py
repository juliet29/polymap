from dataclasses import dataclass

from loguru import logger
from utils4plans.lists import get_unique_one

from polyfix.geometry.layout import Layout
from polyfix.geometry.modify.update import Move
from polyfix.geometry.modify.validate import InvalidPolygonError
from polyfix.geometry.surfaces import Surface
from polyfix.reconcile.gaps import Gap, find_gaps
from polyfix.reconcile.metrics import (
    adjacency_graph,
    graph_edit_distance,
    is_valid,
    room_metrics,
)
from polyfix.reconcile.move_segment import move_segment
from polyfix.reconcile.split import split_surface

TOL = 1e-6
MAX_PASSES = 100


@dataclass
class Repair:
    layout: Layout
    moved_domain: str
    cost: float

    def summary(self) -> str:
        return f"moved {self.moved_domain} (cost={self.cost:.4f})"


def replace_domain(layout: Layout, moved) -> Layout:
    return Layout([moved if d.name == moved.name else d for d in layout.domains])


def apply_side(layout: Layout, side: Surface, gap: Gap, delta: float) -> Layout:
    dom = layout.get_domain(side.domain_name)
    surf = dom.get_surface_by_name(side.name_w_domain)
    at = [
        x
        for x in (gap.overlap.min, gap.overlap.max)
        if surf.range.min + TOL < x < surf.range.max - TOL
    ]
    if at:
        dom = split_surface(dom, surf, at)
        surf = get_unique_one(
            dom.surfaces,
            lambda s: (
                s.direction.name == side.direction.name
                and abs(s.location - side.location) < TOL
                and s.range.min >= gap.overlap.min - TOL
                and s.range.max <= gap.overlap.max + TOL
            ),
        )
    return replace_domain(layout, move_segment(Move(dom, surf, delta)))


def repair_cost(before: Layout, after: Layout, domain_name: str) -> float:
    b = room_metrics(before)[domain_name]
    a = room_metrics(after)[domain_name]
    d_area = abs(a["area"] - b["area"]) / b["area"]
    d_shape = abs(a["shape_factor"] - b["shape_factor"]) / b["shape_factor"]
    return 0.5 * d_area + 0.5 * d_shape


def best_repair(layout: Layout, gap: Gap, gap_kwargs: dict) -> Repair | None:
    g_before = adjacency_graph(layout)
    n_before = len(find_gaps(layout, **gap_kwargs))
    repairs: list[Repair] = []
    for side, delta in ((gap.surface, gap.distance), (gap.neighbor, -gap.distance)):
        try:
            after = apply_side(layout, side, gap, delta)
        except (InvalidPolygonError, ValueError, AssertionError) as e:
            logger.debug(f"candidate {side.name_w_domain} failed: {e}")
            continue
        ok, _ = is_valid(after)
        if not ok:
            continue
        if graph_edit_distance(g_before, adjacency_graph(after)) != 0:
            continue
        if len(find_gaps(after, **gap_kwargs)) >= n_before:
            continue
        repairs.append(Repair(after, side.domain_name, repair_cost(layout, after, side.domain_name)))

    if not repairs:
        return None
    repairs.sort(key=lambda r: (r.cost, r.moved_domain))
    return repairs[0]


def close_gaps(layout: Layout, **gap_kwargs) -> Layout:
    skipped: set[tuple[str, str]] = set()

    def key(g: Gap):
        return (g.surface.name_w_domain, g.neighbor.name_w_domain)

    for _ in range(MAX_PASSES):
        remaining = [g for g in find_gaps(layout, **gap_kwargs) if key(g) not in skipped]
        if not remaining:
            return layout
        gap = remaining[0]
        repair = best_repair(layout, gap, gap_kwargs)
        if repair is None:
            logger.warning(f"no topology-preserving repair for {gap.summary()}; skipping")
            skipped.add(key(gap))
            continue
        logger.info(f"closed {gap.summary()}: {repair.summary()}")
        layout = repair.layout

    logger.warning(f"close_gaps hit MAX_PASSES={MAX_PASSES}")
    return layout
