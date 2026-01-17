from utils4plans.paths import StaticPaths
import pyprojroot

BASE_PATH = pyprojroot.find_root(pyprojroot.has_dir(".git"))

static_paths = StaticPaths(name="", base_path=BASE_PATH)


class DynamicPaths:

    MSD_PATHS = static_paths.inputs / "msd"
    example_paths = static_paths.inputs / "examples"
    msd_outputs = static_paths.temp / "msd"
