"""Entry point for the command-line interface."""

import warnings
from argparse import ArgumentParser
from pathlib import Path
from sys import exit

from sfapp.classes.singlefileappbuilder import SingleFileAppBuilder
from sfapp.showwarning import showwarning


def main():
    warnings.showwarning = showwarning

    parser = ArgumentParser(
        description="Build a single-file app from a Python package."
    )
    parser.add_argument("root", type=Path, help="Root directory of the package.")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path("-"),
        help="Output file (default stdout). Use '-' for stdout.",
    )
    parser.add_argument(
        "-p",
        "--package",
        type=str,
        help="Root package name (defaults to directory name).",
    )
    parser.add_argument(
        "-s", "--silent", action="store_true", help="Disable verbose logging."
    )
    args = parser.parse_args()

    root = args.root.resolve()
    pkg = args.package or root.name
    to_stdout = args.output == Path("-")
    builder = SingleFileAppBuilder(
        root=root,
        package=pkg,
        silent=args.silent,
        to_stdout=to_stdout,
    )
    builder.build(args.output)


if __name__ == "__main__":
    exit(main())
