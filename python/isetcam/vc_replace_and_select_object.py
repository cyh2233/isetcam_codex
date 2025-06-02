# mypy: ignore-errors
"""Replace an object and explicitly set it as selected."""

from __future__ import annotations

from typing import Any, Optional

from .ie_init_session import vcSESSION
from .vc_replace_object import vc_replace_object
from .vc_add_and_select_object import _norm_objtype


def vc_replace_and_select_object(
    obj_type: str, obj: Any, index: Optional[int] = None
) -> int:
    """Replace ``obj`` and select it in ``vcSESSION``.

    Parameters
    ----------
    obj_type : str
        Type of the object.
    obj : Any
        The new object instance.
    index : int, optional
        1-based index to replace.  Uses the currently selected index when not
        provided.

    Returns
    -------
    int
        The index that was replaced and selected.
    """
    idx = vc_replace_object(obj_type, obj, index)
    field = _norm_objtype(obj_type)
    vcSESSION.setdefault("SELECTED", {})[field] = idx
    return idx
