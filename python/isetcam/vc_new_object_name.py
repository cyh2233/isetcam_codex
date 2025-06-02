# mypy: ignore-errors
"""Generate a new default name for an object type."""

from __future__ import annotations

from .vc_count_objects import vc_count_objects
from .vc_add_and_select_object import _norm_objtype


def vc_new_object_name(obj_type: str) -> str:
    """Return a new name for ``obj_type`` based on current count."""
    field = _norm_objtype(obj_type)
    idx = vc_count_objects(obj_type) + 1
    return f"{field}{idx}"

