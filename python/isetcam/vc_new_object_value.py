"""Compute the next available numeric identifier for an object type."""

from __future__ import annotations

from typing import Tuple, Union

from .ie_init_session import vcSESSION
from .vc_add_and_select_object import _norm_objtype
from .vc_count_objects import vc_count_objects


def vc_new_object_value(obj_type: str) -> Union[int, Tuple[int, int, int]]:
    """Return the next numeric identifier for ``obj_type``.

    For cameras the return value is a 3-tuple with the next identifiers for
    the optical image, sensor and image processor objects that compose the
    camera.
    """
    field = _norm_objtype(obj_type)
    if field == "CAMERA":
        oi_val = vc_count_objects("opticalimage") + 1
        sensor_val = vc_count_objects("sensor") + 1
        ip_list = vcSESSION.get("VCIMAGE", [None])
        if len(ip_list) == 1 and ip_list[0] is None:
            ip_val = 1
        else:
            ip_val = len(ip_list)
        return oi_val, sensor_val, ip_val

    return vc_count_objects(obj_type) + 1

