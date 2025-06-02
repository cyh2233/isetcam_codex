# mypy: ignore-errors
"""Replace an existing object in ``vcSESSION`` and mark it selected."""

from __future__ import annotations

from typing import Any, Optional

from .ie_init_session import vcSESSION
from .vc_add_and_select_object import _norm_objtype


def vc_replace_object(obj_type: str, obj: Any, index: Optional[int] = None) -> int:
    """Replace an object stored in ``vcSESSION``.

    Parameters
    ----------
    obj_type : str
        Object type to replace.
    obj : Any
        Replacement object instance.
    index : int, optional
        1-based index of the object to replace.  When omitted the currently
        selected index is used and if none exists ``1`` is assumed.

    Returns
    -------
    int
        The index of the replaced object.
    """
    field = _norm_objtype(obj_type)

    if index is None:
        index = vcSESSION.get("SELECTED", {}).get(field)
        if index is None:
            index = 1

    lst = vcSESSION.setdefault(field, [None])
    while len(lst) <= index:
        lst.append(None)
    lst[index] = obj
    vcSESSION[field] = lst

    vcSESSION.setdefault("SELECTED", {})[field] = index
    return index
