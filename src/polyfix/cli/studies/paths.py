from pathlib import Path

import pyprojroot

BASE_PATH = pyprojroot.find_root(pyprojroot.has_dir(".git"))
TEMP_PATH = "/scratch/users/jnwagwu/polyfix"


class StaticPaths:
    inputs = Path(BASE_PATH) / "static/1_inputs"
    temp = Path(TEMP_PATH) / "4_temp"
    figures = Path(TEMP_PATH) / "figures"


class MSDPaths:
    base = StaticPaths.inputs
    basic = base / "msd"
    hard = base / "msd_hard"


class ExternalMSDPaths:
    base = Path("/scratch/users/jnwagwu/msd2/test_msd/")
    proc = base / "processed"


class SVGPaths:
    base = StaticPaths.temp / "svgs"
    ablation_c = base / "ablation_c/init"


class Inputs:
    msd = MSDPaths
    ext_msd = ExternalMSDPaths
    svg = SVGPaths


class Temp:
    base = StaticPaths.temp
    generated = base / "generated_out"
    msd = base / "msd_out"
    svg = base / "svg_out"


class ProjectPaths:
    inputs = Inputs
    temp = Temp
