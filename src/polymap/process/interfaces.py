from typing import NamedTuple

from polymap.interfaces import GraphPairs
from polymap.layout.interfaces import Layout


class ProcessLayouts(NamedTuple):
    id: str
    original: Layout = Layout([])
    rotated: Layout = Layout([])
    ortho: Layout = Layout([])
    simplified: Layout = Layout([])
    xpull: Layout = Layout([])
    ypull: Layout = Layout([])

    @property
    def titles(self):
        return list(self._asdict().keys())


class ProcessGraphPairs(NamedTuple):
    x: GraphPairs = dict()
    y: GraphPairs = dict()
