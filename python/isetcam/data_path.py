from __future__ import annotations

from pathlib import Path
import importlib.resources as resources
import base64
import tempfile

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
        b64_file = candidate.with_suffix(candidate.suffix + '.b64')
        if b64_file.exists():
            tmp_root = Path(tempfile.gettempdir()) / 'isetcam_data'
            tmp_path = tmp_root / rel
            if not tmp_path.exists():
                tmp_path.parent.mkdir(parents=True, exist_ok=True)
                data = base64.b64decode(b64_file.read_text())
                with open(tmp_path, 'wb') as f:
                    f.write(data)
            return tmp_path
    except ModuleNotFoundError:
        pass
    return iset_root_path() / 'data' / rel
