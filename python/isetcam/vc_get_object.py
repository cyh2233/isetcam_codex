# mypy: ignore-errors
"""Retrieve objects from ``vcSESSION`` by type and index."""

from __future__ import annotations

from typing import Any, Optional

from .ie_init_session import vcSESSION
from .vc_add_and_select_object import _norm_objtype


def vc_get_object(obj_type: str, index: Optional[int] = None) -> Any:
    """Return an object stored in ``vcSESSION``.

    Parameters
    ----------
    obj_type : str
        The type of object (e.g. ``'scene'`` or ``'sensor'``).
    index : int, optional
        1-based index of the object.  When omitted the currently selected
        object is returned.
    """
    field = _norm_objtype(obj_type)

    if index is None:
        index = vcSESSION.get("SELECTED", {}).get(field)
        if index is None:
            return None

    lst = vcSESSION.get(field)
    if not lst or index >= len(lst) or index < 0:
        return None

    return lst[index]
