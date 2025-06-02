# mypy: ignore-errors
"""Return the index and object currently selected in ``vcSESSION``."""

from __future__ import annotations

from typing import Any, Optional, Tuple

from .ie_init_session import vcSESSION
from .vc_add_and_select_object import _norm_objtype
from .vc_get_object import vc_get_object


def vc_get_selected_object(obj_type: str) -> tuple[Optional[int], Any]:
    """Return the selected index and object of ``obj_type``."""
    field = _norm_objtype(obj_type)
    index = vcSESSION.get("SELECTED", {}).get(field)
    if index is None:
        return None, None
    return index, vc_get_object(obj_type, index)

