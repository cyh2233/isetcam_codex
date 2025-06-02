# mypy: ignore-errors
"""Compute camera metrics by name."""

from __future__ import annotations

from typing import Any, Callable

from ..camera import (
    Camera,
    camera_color_accuracy,
    camera_mtf,
    camera_full_reference,
    camera_moire,
    camera_vsnr_sl,
    camera_acutance,
)
from ..ie_param_format import ie_param_format


_METRIC_FUNCS: dict[str, Callable[..., Any]] = {
    "mcccolor": camera_color_accuracy,
    "slantededge": camera_mtf,
    "fullreference": camera_full_reference,
    "moire": camera_moire,
    "vsnr": camera_vsnr_sl,
    "acutance": camera_acutance,
}


def metrics_camera(camera: Camera, metric_name: str, *args: Any, **kwargs: Any) -> Any:
    """Return a camera metric specified by ``metric_name``.

    Parameters
    ----------
    camera : :class:`~isetcam.camera.Camera`
        Camera object to evaluate.
    metric_name : str
        Name identifying which metric to compute.
    *args, **kwargs : Any
        Additional parameters forwarded to the specific metric function.

    Returns
    -------
    Any
        Result produced by the selected metric function.
    """
    if camera is None:
        raise ValueError("camera is required")
    if not metric_name:
        raise ValueError("metric_name must be defined")

    key = ie_param_format(metric_name)
    func = _METRIC_FUNCS.get(key)
    if func is None:
        raise ValueError(f"Unknown metric '{metric_name}'")
    return func(camera, *args, **kwargs)


__all__ = ["metrics_camera"]

