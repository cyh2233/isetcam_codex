# mypy: ignore-errors
"""Add an object to ``vcSESSION`` and set it as selected."""

from __future__ import annotations

from typing import Any

from .ie_init_session import vcSESSION

_OBJTYPE_MAP = {
    "scene": "SCENE",
    "opticalimage": "OPTICALIMAGE",
    "oi": "OPTICALIMAGE",
    "sensor": "ISA",
    "isa": "ISA",
    "display": "DISPLAY",
    "camera": "CAMERA",
}


def _norm_objtype(name: str) -> str:
    key = name.lower()
    if key not in _OBJTYPE_MAP:
        raise KeyError(f"Unknown object type '{name}'")
    return _OBJTYPE_MAP[key]


def vc_add_and_select_object(obj_type: str, obj: Any) -> int:
    """Store ``obj`` in ``vcSESSION`` under ``obj_type`` and select it."""
    field = _norm_objtype(obj_type)

    lst = vcSESSION.setdefault(field, [None])
    lst.append(obj)
    index = len(lst) - 1
    vcSESSION[field] = lst

    selected = vcSESSION.setdefault("SELECTED", {})
    selected[field] = index
    return index

