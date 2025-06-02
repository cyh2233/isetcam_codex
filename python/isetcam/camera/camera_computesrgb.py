# mypy: ignore-errors
"""Compute simple sRGB rendering for a camera scene pair."""

from __future__ import annotations

from typing import Optional

import numpy as np

try:  # pragma: no cover - matplotlib might not be installed
    import matplotlib.pyplot as plt
except Exception:  # pragma: no cover - matplotlib might not be installed
    plt = None  # type: ignore

from .camera_class import Camera
from .camera_compute import camera_compute
from ..scene import Scene, scene_create, scene_adjust_luminance
from ..quanta2energy import quanta_to_energy
from ..ie_xyz_from_energy import ie_xyz_from_energy
from ..srgb_xyz import xyz_to_srgb
from ..ie_format_figure import ie_format_figure


_DEF_SCENE = "macbeth d65"
_DEF_LUM = 100.0
_DEF_FOV = 10.0
_DEF_PATCH = 16


def camera_computesrgb(
    camera: Camera,
    scene: Scene | str | None = None,
    *,
    mean_luminance: float = _DEF_LUM,
    fov: float = _DEF_FOV,
    patch_size: int = _DEF_PATCH,
    plot: bool = False,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return an sRGB rendering of ``scene`` captured by ``camera``.

    Parameters
    ----------
    camera : Camera
        Camera instance to use for rendering.
    scene : Scene or str or None, optional
        Scene to render. When a string or ``None`` a new scene is created
        using :func:`scene_create`.  ``None`` defaults to ``"macbeth d65"``.
    mean_luminance : float, optional
        Target mean luminance for the scene. Default is ``100``.
    fov : float, optional
        Field of view assigned to the scene in degrees. Default is ``10``.
    patch_size : int, optional
        Patch size passed to :func:`scene_create` when ``scene`` is a string
        or ``None``. Default is ``16``.
    plot : bool, optional
        Display the resulting sRGB image using Matplotlib.

    Returns
    -------
    srgb_result : np.ndarray
        Approximate sRGB image produced by the camera.
    srgb_ideal : np.ndarray
        Ideal sRGB rendering derived directly from the scene photons.
    raw_volts : np.ndarray
        Sensor voltage image after calling :func:`camera_compute`.
    """

    if scene is None or isinstance(scene, str):
        name = _DEF_SCENE if scene is None else scene
        sc = scene_create(name, patch_size=patch_size)
    else:
        sc = scene

    sc = scene_adjust_luminance(sc, "mean", float(mean_luminance))
    sc.fov = float(fov)

    camera_compute(camera, sc)
    volts = camera.sensor.volts.astype(float)

    # Ideal sRGB rendering from the scene
    energy = quanta_to_energy(sc.wave, sc.photons)
    xyz = ie_xyz_from_energy(energy, sc.wave)
    srgb_ideal, _, _ = xyz_to_srgb(xyz)

    # Camera result scaled to [0, 1] and replicated across channels
    scaled = volts / volts.max() if volts.max() > 0 else volts
    srgb_result = np.repeat(scaled[:, :, None], 3, axis=2)

    if plot:
        if plt is None:
            raise ImportError("matplotlib is required for plotting")
        fig, ax = plt.subplots()
        ax.imshow(np.clip(srgb_result, 0.0, 1.0))
        ax.axis("off")
        ie_format_figure(ax)

    return srgb_result, srgb_ideal, volts.copy()


__all__ = ["camera_computesrgb"]
