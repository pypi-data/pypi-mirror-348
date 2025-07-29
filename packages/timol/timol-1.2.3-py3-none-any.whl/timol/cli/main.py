import argparse

from importlib_resources import files

from timol.main import Timol
from timol.reader import MoleculesReader


def cli():
    args = parse_args()
    run_timol(args)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "file",
        help="Path to the file to be read (e.g. xyz file). Replace with `test` to try a testing xyz file, replace with `bigtest` to try testing a large xyz file",
    )
    parser.add_argument(
        "-i",
        "--index",
        help="Additional index argument to be assed to ase's read function, using ase's syntax. For example, use `-1` for the last frame or `:10` for the first 10. Only works for file formats where ase supports indexing",
        required=False,
        default=":",
    )
    parser.add_argument(
        "-b", "--bmark", help="Benchmark the run", default=False, action="store_true"
    )

    args = parser.parse_args()

    return args


def run_timol(args: argparse.Namespace):
    path = args.file

    if path == "test":
        path = files("timol").joinpath("test_xyz.xyz")

    if path == "bigtest":
        path = files("timol").joinpath("R_hemo.xyz")

    mr = MoleculesReader(path, index=args.index)
    app = Timol(mr, bmark=args.bmark)
    reply = app.run()

    if app.bmarker is not None:
        app.bmarker.generic_print()
