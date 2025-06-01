"""Retrieve the list of objects for a given type from ``vcSESSION``."""

from __future__ import annotations

from typing import Any, List

from .ie_init_session import vcSESSION
from .vc_add_and_select_object import _norm_objtype


def vc_get_objects(obj_type: str) -> list[Any]:
    """Return the stored list of objects for ``obj_type``.

    Parameters
    ----------
    obj_type : str
        The object type (e.g. ``'scene'`` or ``'sensor'``).

    Returns
    -------
    list[Any]
        The list of objects. If none exist a list with a single ``None``
        placeholder is returned.
    """
    field = _norm_objtype(obj_type)
    return vcSESSION.get(field, [None])

