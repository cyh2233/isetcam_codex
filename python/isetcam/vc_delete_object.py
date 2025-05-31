"""Delete an object stored in ``vcSESSION``."""

from __future__ import annotations

from typing import Optional

from .ie_init_session import vcSESSION
from .vc_add_and_select_object import _norm_objtype


def vc_delete_object(obj_type: str, index: Optional[int] = None) -> int:
    """Remove an object from ``vcSESSION``.

    Parameters
    ----------
    obj_type : str
        Object type to remove (e.g. ``'scene'`` or ``'sensor'``).
    index : int, optional
        1-based index of the object.  When omitted the currently selected
        object of ``obj_type`` is deleted.

    Returns
    -------
    int
        The number of remaining objects of ``obj_type``.
    """
    field = _norm_objtype(obj_type)

    if index is None:
        index = vcSESSION.get("SELECTED", {}).get(field)
        if index is None:
            return 0

    lst = vcSESSION.get(field)
    if not lst or index <= 0 or index >= len(lst):
        raise IndexError("Index out of range")

    lst.pop(index)
    vcSESSION[field] = lst

    remaining = len(lst) - 1

    selected = vcSESSION.setdefault("SELECTED", {})
    cur_sel = selected.get(field)
    if cur_sel is not None:
        if cur_sel == index:
            if remaining == 0:
                selected[field] = []
            else:
                selected[field] = min(index - 1, remaining)
        elif cur_sel > index:
            selected[field] = cur_sel - 1

    return remaining
