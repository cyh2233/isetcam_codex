# mypy: ignore-errors
"""Count objects of a given type stored in ``vcSESSION``."""

from __future__ import annotations

from .vc_get_objects import vc_get_objects


def vc_count_objects(obj_type: str) -> int:
    """Return the number of stored objects of ``obj_type``."""
    objs = vc_get_objects(obj_type)
    if len(objs) == 1 and objs[0] is None:
        return 0
    return len(objs) - 1

