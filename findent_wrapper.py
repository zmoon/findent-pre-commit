"""
"Findent reads from STDIN, writes to STDOUT."
This wrapper facilitates passing a file path and modifying that file.
"""
from __future__ import annotations

from pathlib import Path


def format_with_findent(orig: str, *, args: list[str] | None = None) -> str:
    import subprocess

    cmd = ["findent"]
    if args is not None:
        cmd.extend(args)
    # print(cmd)
    cp = subprocess.run(cmd, check=True, input=orig, capture_output=True, text=True)

    return cp.stdout


def cli():
    import argparse

    parser = argparse.ArgumentParser(description="format a file in-place with findent",
        epilog=(
            "IMPORTANT: wrapper-specific arguments like `--diff` must precede the file name, "
            "since everything following the file name is passed to findent."
        ),
    )
    parser.add_argument(
        "file",
        metavar="FILE",
        type=str,
        nargs="?",
        default=None,
        help="file to format (path)",
    )
    parser.add_argument(
        "--diff",
        action="store_true",
        help="print diff instead of modifying the file",
    )
    parser.add_argument(
        "--findent-help",
        action="store_true",
        help="print findent help (`findent --help`) and exit",
    )
    parser.add_argument(
        "findent_args",
        metavar="FINDENT-ARGS",
        nargs=argparse.REMAINDER,
        help="additional arguments (...) are passed to findent. Must follow wrapper-specific arguments!",
    )
    # TODO: try intermixed parse?
    args = parser.parse_args()
    # print(args)

    # TODO: main() fn
    if args.findent_help:
        import subprocess

        subprocess.run(["findent", "--help"])
        return 0

    if args.file is None:
        print("error: must pass file to be formatted")
        parser.print_usage()
        return 2

    p = Path(args.file)
    if not p.is_file():
        print(f"error: file {p} does not exist")
        return 2

    with open(p, "r") as f:
        orig = f.read()

    new = format_with_findent(orig, args=args.findent_args)

    if args.diff:
        import difflib

        diff = difflib.unified_diff(
            orig.splitlines(), new.splitlines(), lineterm="",
        )
        print("\n".join(diff))
        return 0

    else:
        with open(p, "w") as f:
            f.write(new)

    # TODO: --check option?


if __name__ == "__main__":
    cli()
