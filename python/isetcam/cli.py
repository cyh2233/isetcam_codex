"""Command line interface for ISETCam utilities."""

from __future__ import annotations

import argparse
import subprocess
import sys

import isetcam




def _cmd_info(args: argparse.Namespace) -> int:
    """Print package version and repository root."""
    print(f"isetcam {isetcam.__version__}")
    print(isetcam.iset_root_path())
    return 0


def _cmd_list_scenes(args: argparse.Namespace) -> int:
    """List sample scene names."""
    from isetcam.scene import scene_list

    for name in scene_list():
        print(name)
    return 0


def _cmd_run_tests(args: argparse.Namespace) -> int:
    """Run the Python unit tests using pytest."""
    root = isetcam.iset_root_path()
    cmd = [sys.executable, "-m", "pytest", "-q"]
    result = subprocess.run(cmd, cwd=root)
    return result.returncode


def main(argv: list[str] | None = None) -> int:
    """Entry point for the ``isetcam`` command."""
    parser = argparse.ArgumentParser(prog="isetcam")
    subparsers = parser.add_subparsers(dest="command")

    p_info = subparsers.add_parser("info", help="Show version information")
    p_info.set_defaults(func=_cmd_info)

    p_list = subparsers.add_parser("list-scenes", help="List available scenes")
    p_list.set_defaults(func=_cmd_list_scenes)

    p_tests = subparsers.add_parser("run-tests", help="Run the unit tests")
    p_tests.set_defaults(func=_cmd_run_tests)

    args = parser.parse_args(argv)
    if not hasattr(args, "func"):
        parser.print_help()
        return 0
    return args.func(args)


if __name__ == "__main__":  # pragma: no cover - script entry
    sys.exit(main())
