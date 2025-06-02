# mypy: ignore-errors
"""Update the selected object index for a given type in ``vcSESSION``."""

from __future__ import annotations

from typing import Optional

from .ie_init_session import vcSESSION
from .vc_add_and_select_object import _norm_objtype
from .vc_get_objects import vc_get_objects


def vc_set_selected_object(obj_type: str, index: Optional[int]) -> None:
    """Set the selected index for ``obj_type``."""
    field = _norm_objtype(obj_type)
    if index is None or index < 1:
        vcSESSION.setdefault("SELECTED", {})[field] = []
        return

    objs = vc_get_objects(obj_type)
    count = len(objs) - 1 if not (len(objs) == 1 and objs[0] is None) else 0
    if index > count:
        raise IndexError("Selected object out of range")
    vcSESSION.setdefault("SELECTED", {})[field] = index

