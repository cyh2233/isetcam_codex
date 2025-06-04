# mypy: ignore-errors
"""Load an ISET object from a MAT-file."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from scipy.io import loadmat


_OBJ_MAP = {
    "scene": "scene",
    "opticalimage": "opticalimage",
    "oi": "opticalimage",
    "isa": "sensor",
    "sensor": "sensor",
    "vcimage": "vcimage",
    "pixel": "pixel",
    "optics": "optics",
    "camera": "camera",
}


def vc_import_object(obj_type: str, path: str | Path) -> Any:
    """Return the object stored in ``path`` of type ``obj_type``."""
    key = _OBJ_MAP.get(obj_type.lower())
    if key is None:
        raise KeyError(f"unknown object type '{obj_type}'")
    data = loadmat(str(Path(path)), squeeze_me=True, struct_as_record=False)
    if key not in data:
        raise KeyError(f"file does not contain '{key}' variable")
    return data[key]


__all__ = ["vc_import_object"]
