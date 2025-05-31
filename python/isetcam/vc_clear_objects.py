"""Clear stored objects in ``vcSESSION``."""

from __future__ import annotations

from .ie_init_session import vcSESSION

# Fields in ``vcSESSION`` that hold lists of objects
_OBJECT_FIELDS = [
    "SCENE",
    "OPTICALIMAGE",
    "ISA",
    "VCIMAGE",
    "DISPLAY",
    "GRAPHWIN",
    "CAMERA",
]


def vc_clear_objects() -> None:
    """Remove all objects and reset selection indices."""

    for field in _OBJECT_FIELDS:
        if field == "GRAPHWIN":
            vcSESSION[field] = []
        else:
            vcSESSION[field] = [None]

    selected = vcSESSION.setdefault("SELECTED", {})
    for field in _OBJECT_FIELDS:
        selected[field] = []
