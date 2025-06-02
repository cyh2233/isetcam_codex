# mypy: ignore-errors
"""Rename an object stored in ``vcSESSION``."""

from __future__ import annotations

from typing import Optional

from .ie_init_session import vcSESSION
from .vc_add_and_select_object import _norm_objtype


def vc_rename_object(obj_type: str, new_name: str, index: Optional[int] = None) -> None:
    """Change the ``name`` attribute for a stored object.

    Parameters
    ----------
    obj_type : str
        Type of the object to rename.
    new_name : str
        The new name to assign.
    index : int, optional
        1-based index of the object.  When omitted the currently selected
        object is renamed.
    """
    field = _norm_objtype(obj_type)

    if index is None:
        index = vcSESSION.get("SELECTED", {}).get(field)
        if index is None:
            raise IndexError("No selected object to rename")

    lst = vcSESSION.get(field)
    if not lst or index <= 0 or index >= len(lst):
        raise IndexError("Index out of range")

    obj = lst[index]
    if not hasattr(obj, "name"):
        raise AttributeError("Object has no name attribute")
    setattr(obj, "name", new_name)
