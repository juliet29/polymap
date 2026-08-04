from dataclasses import dataclass
from pathlib import Path


@dataclass
class SingleWorkflowPaths:
    base: Path

    @property
    def init(self):
        return self.base / "init/out.json"

    @property
    def rotate(self):
        return self.base / "rotate/out.json"

    @property
    def ortho(self):
        return self.base / "ortho/out.json"

    @property
    def simplify(self):
        return self.base / "simplify/out.json"

    @property
    def xplan(self):
        return self.base / "xplan/out.json"

    @property
    def xmove(self):
        return self.base / "xmove/out.json"

    @property
    def yplan(self):
        return self.base / "yplan/out.json"

    @property
    def ymove(self):
        return self.base / "ymove/out.json"

    @property
    def reconcile(self):
        return self.base / "reconcile/out.json"

    @property
    def adjacencies(self):
        return self.base / "out.adj.yaml"

    ## take 2: -----------
    def xplan_i(self, i: int = 1):
        return self.base / f"xplan_{i}/out.json"

    def yplan_i(self, i: int = 1):
        return self.base / f"yplan_{i}/out.json"
