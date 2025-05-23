"""Modify values in the global ISETCam session."""

from __future__ import annotations

from typing import Any

from .ie_init_session import vcSESSION, ISET_PREFS
from .ie_param_format import ie_param_format


_OBJTYPE_MAP = {
    "scene": "SCENE",
    "oi": "OPTICALIMAGE",
    "opticalimage": "OPTICALIMAGE",
    "sensor": "ISA",
    "isa": "ISA",
    "vcimage": "VCIMAGE",
    "ip": "VCIMAGE",
    "display": "DISPLAY",
}


def _norm_objtype(name: str) -> str:
    key = ie_param_format(name)
    if key not in _OBJTYPE_MAP:
        raise KeyError(f"Unknown object type '{name}'")
    return _OBJTYPE_MAP[key]


def ie_session_set(param: str, val: Any, *args: Any) -> None:
    """Set a value in the global ``vcSESSION`` or ``ISET_PREFS``."""
    p = ie_param_format(param)

    if p == "version":
        vcSESSION["VERSION"] = val
        return
    if p in {"name", "sessionname"}:
        vcSESSION["NAME"] = val
        return
    if p in {"dir", "sessiondir"}:
        vcSESSION["DIR"] = val
        return
    if p == "waitbar":
        ISET_PREFS["waitbar"] = int(bool(val))
        vcSESSION.setdefault("GUI", {})["waitbar"] = int(bool(val))
        return
    if p in {"fontsize", "font size"}:
        ISET_PREFS["fontSize"] = val
        return
    if p in {"initclear", "init clear"}:
        ISET_PREFS["initClear"] = int(bool(val))
        return

    if p == "selected":
        if not args:
            raise ValueError("Object type required for 'selected'")
        obj = _norm_objtype(str(args[0]))
        vcSESSION.setdefault("SELECTED", {})[obj] = val
        return

    if p in _OBJTYPE_MAP:
        obj = _norm_objtype(p)
        vcSESSION.setdefault("SELECTED", {})[obj] = val
        return

    raise KeyError(f"Unknown session parameter '{param}'")
