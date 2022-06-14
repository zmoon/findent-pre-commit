"""
Wrapper to apply the findent Fortran code formatter.

"Findent reads from STDIN, writes to STDOUT."
This wrapper facilitates in-place modification.
"""
from __future__ import annotations

import logging
import os
import sys
from pathlib import Path


logging.basicConfig(stream=sys.stdout)
logger = logging.getLogger(__name__)

__version__ = "0.1.0.dev0"

FINDENT_PATH = os.environ.get("FINDENT", "findent")


def format_with_findent(orig: str, *, args: list[str] | None = None) -> str:
    import subprocess

    cmd = [FINDENT_PATH]
    if args is not None:
        cmd.extend(args)
    logger.debug(f"cmd: {cmd}")
    cp = subprocess.run(cmd, check=True, input=orig, capture_output=True, text=True)

    return cp.stdout


def cli() -> int:
    import argparse

    parser = argparse.ArgumentParser(
        description="format files in-place with findent",
        epilog=(
            "NOTE: although it is not required, for clarity, "
            "wrapper-specific arguments like `--diff` should precede file names, "
            "and findent arguments like `-i3` should follow the follow names."
        ),  # or the other way around?
    )
    parser.add_argument(
        "files",
        metavar="FILES",
        type=str,
        nargs="*",
        help="files to format (paths)",
    )
    parser.add_argument(
        "--diff",
        action="store_true",
        help="print diff instead of modifying",
    )
    parser.add_argument(
        "--findent-help",
        action="store_true",
        help="print findent help (`findent --help`) and exit",
    )
    parser.add_argument(
        "--findent-version-pin",
        help="error if the detected findent is not this version",
        default=None,
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="print findent-wrapper debug messages",
    )
    args, findent_args = parser.parse_known_intermixed_args()

    if args.debug:
        import shutil

        logger.setLevel(logging.DEBUG)
        logger.debug(f"findent path setting: {FINDENT_PATH}")
        logger.debug(f"findent absolute path: {shutil.which(FINDENT_PATH)}")

    logger.debug(f"parsed args: {args}")
    logger.debug(f"findent (extra) args: {findent_args}")

    # TODO: main() fn
    if args.findent_help:
        import subprocess

        subprocess.run([FINDENT_PATH, "--help"])
        return 0

    if args.findent_version_pin:
        import subprocess

        cp = subprocess.run(["findent", "--version"], check=True, text=True, capture_output=True)
        v = cp.stdout.split()[2]
        if v != args.findent_version_pin:
            print(
                f"error: findent-version-pin is {args.findent_version_pin!r}, "
                f"but detected findent version is {v!r}"
            )
            return 1

    if not args.files:
        print("error: must pass file(s) to be formatted")
        parser.print_usage()
        return 2

    for fp in args.files:
        p = Path(fp)
        if not p.is_file():
            print(f"error: file {p} does not exist")
            return 2

        with open(p, "r") as f:
            orig = f.read()

        new = format_with_findent(orig, args=findent_args)

        if args.diff:
            import difflib

            diff = difflib.unified_diff(
                orig.splitlines(), new.splitlines(), lineterm="", fromfile=str(p)
            )
            print("\n".join(diff))

        else:
            with open(p, "w") as f:
                f.write(new)

        # TODO: --check option?

    return 0


if __name__ == "__main__":
    cli()
