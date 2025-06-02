# mypy: ignore-errors
"""List the names of stored objects of a given type."""

from __future__ import annotations

from typing import List
import warnings

from .vc_get_objects import vc_get_objects


def vc_get_object_names(obj_type: str, make_unique: bool = False) -> list[str]:
    """Return the object names for ``obj_type``.

    Parameters
    ----------
    obj_type : str
        Object type to query.
    make_unique : bool, optional
        When ``True`` prefix the names with their index to ensure
        uniqueness.
    """
    objs = vc_get_objects(obj_type)
    if len(objs) == 1 and objs[0] is None:
        return []

    names: list[str] = []
    for idx, obj in enumerate(objs[1:], start=1):
        if obj is None:
            continue
        name = getattr(obj, "name", None)
        if name is None:
            warnings.warn("Missing object name", RuntimeWarning)
            continue
        names.append(name)

    if make_unique:
        names = [f"{i}-{n}" for i, n in enumerate(names, start=1)]
    return names

