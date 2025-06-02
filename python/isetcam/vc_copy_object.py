# mypy: ignore-errors
"""Copy an object entry from ``vcSESSION``."""

from __future__ import annotations

from typing import Any, Optional
import copy

from .ie_init_session import vcSESSION
from .vc_add_and_select_object import _norm_objtype


def vc_copy_object(obj_type: str, index: Optional[int] = None) -> int:
    """Duplicate an object stored in ``vcSESSION``.

    Parameters
    ----------
    obj_type : str
        Type of object to copy.
    index : int, optional
        1-based index of the object to copy.  When omitted the currently
        selected object is duplicated.

    Returns
    -------
    int
        The index of the newly inserted copy.
    """
    field = _norm_objtype(obj_type)

    if index is None:
        index = vcSESSION.get("SELECTED", {}).get(field)
        if index is None:
            raise IndexError("No selected object to copy")

    lst = vcSESSION.get(field)
    if not lst or index <= 0 or index >= len(lst):
        raise IndexError("Index out of range")

    obj = lst[index]
    copied = copy.deepcopy(obj)
    lst.append(copied)
    new_idx = len(lst) - 1
    vcSESSION[field] = lst
    return new_idx
