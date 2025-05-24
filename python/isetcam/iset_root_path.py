from pathlib import Path


def iset_root_path() -> Path:
    """Return the root directory of the ISETCam project."""
    return Path(__file__).resolve().parents[2]
