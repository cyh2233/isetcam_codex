from __future__ import annotations

from pathlib import Path
import importlib.resources as resources

from .iset_root_path import iset_root_path


def data_path(relative: str | Path) -> Path:
    """Return absolute path to a data file.

    The function first attempts to locate the file within the installed
    ``isetcam.data`` package. If the file is not found there, it falls back
    to the repository ``data`` directory, allowing the code to run from the
    source tree.
    """
    rel = Path(relative)
    try:
        base = resources.files('isetcam.data')
        candidate = Path(base / rel)
        if candidate.exists():
            return candidate
    except ModuleNotFoundError:
        pass
    return iset_root_path() / 'data' / rel
