"""Replace the list of objects stored for a given type in ``vcSESSION``."""

from __future__ import annotations

from typing import Sequence, Any

from .ie_init_session import vcSESSION
from .vc_add_and_select_object import _norm_objtype


def vc_set_objects(obj_type: str, objects: Sequence[Any]) -> None:
    """Set the list of objects for ``obj_type``."""
    field = _norm_objtype(obj_type)
    vcSESSION[field] = list(objects)

