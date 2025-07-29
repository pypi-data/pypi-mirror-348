import argparse

import numpy as np
from importlib_resources import files

from timol.reader import MoleculesReader
from timol.utils import Benchmarker
from timol.viewer import MolViewer


def bmark():
    args = parse_args()
    run_bmark(args)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument("-n", help="Number of iterations", default=100, type=int)

    parser.add_argument(
        "-b",
        "--big",
        help="Benchmark on the big molecule",
        default=False,
        action="store_true",
    )

    parser.add_argument(
        "-m",
        "--mode",
        help="Drawing mode (defaults to spheres)",
        default="spheres",
        type=str,
        choices=["spheres", "lines", "spheres&lines"],
    )
    parser.add_argument(
        "-r", "--radii_scale", help="Radii scale for spheres", default=1, type=float
    )
    parser.add_argument(
        "--width", type=int, help="Width of the imaginary window", default=100
    )
    parser.add_argument(
        "--height", type=int, help="Height of the imaginary window", default=100
    )
    parser.add_argument(
        "-s",
        "--scale",
        type=float,
        help="Scale (=zoom) of the window: larger = more zoomed in",
        default=10,
    )

    args = parser.parse_args()

    return args


def build_matrix_at_index(viewer: MolViewer, index: int):
    viewer.index = index % viewer.mols_reader.get_n_molecules()
    viewer.build_matrix()


def get_benchmark(args: dict) -> Benchmarker:
    if args.get("big", False):
        path = files("timol").joinpath("R_hemo.xyz")

    else:
        path = files("timol").joinpath("test_xyz.xyz")

    bmarker = Benchmarker()
    mr = MoleculesReader(path)
    viewer = MolViewer(
        mr,
        headless=True,
        bmarker=bmarker,
        headless_mode=args["mode"],
        headless_radii_scale=args["radii_scale"],
        headless_size=(args["height"], args["width"]),
        headless_zoom_scale=args["scale"],
    )

    f_args = list(zip([viewer] * args["n"], np.arange(int(args["n"]))))

    bmarker.run_n_times("build_matrix", args["n"], build_matrix_at_index, args=f_args)
    return bmarker


def run_bmark(args: argparse.Namespace):
    bmarker = get_benchmark(vars(args))
    bmarker.generic_print()
