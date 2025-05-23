"""Access values from the global ISETCam session."""

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


def ie_session_get(param: str, *args: Any) -> Any:
    """Return a value from the global ``vcSESSION`` or ``ISET_PREFS``.

    Parameters
    ----------
    param : str
        Name of the session parameter.
    *args : Any
        Additional arguments used by some parameters.
    """
    p = ie_param_format(param)

    if p == "version":
        return vcSESSION.get("VERSION")
    if p in {"name", "sessionname"}:
        return vcSESSION.get("NAME")
    if p in {"dir", "sessiondir"}:
        return vcSESSION.get("DIR")
    if p == "waitbar":
        gui = vcSESSION.get("GUI", {})
        return gui.get("waitbar", ISET_PREFS.get("waitbar", 0))
    if p in {"fontsize", "fontsize", "font size"}:
        return ISET_PREFS.get("fontSize", 12)
    if p in {"initclear", "init clear"}:
        return ISET_PREFS.get("initClear", 0)

    if p == "selected":
        if not args:
            raise ValueError("Object type required for 'selected'")
        obj = _norm_objtype(str(args[0]))
        return vcSESSION.get("SELECTED", {}).get(obj)

    if p in _OBJTYPE_MAP:
        obj = _norm_objtype(p)
        return vcSESSION.get("SELECTED", {}).get(obj)

    raise KeyError(f"Unknown session parameter '{param}'")
