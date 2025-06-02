# mypy: ignore-errors
"""Compute basic full-reference metrics for a camera scene pair."""

from __future__ import annotations

from typing import Any, Dict

import numpy as np

from .camera_class import Camera
from .camera_compute import camera_compute
from .camera_mtf import camera_mtf
from .camera_vsnr import camera_vsnr
from ..scene import Scene
from ..quanta2energy import quanta_to_energy
from ..ie_xyz_from_energy import ie_xyz_from_energy
from ..srgb_xyz import xyz_to_srgb
from ..srgb_to_lab import srgb_to_lab
from ..metrics import delta_e_ab


_WHITEPOINT = np.array([0.95047, 1.0, 1.08883])


def camera_full_reference(camera: Camera, scene: Scene) -> Dict[str, Any]:
    """Return simple full-reference metrics for ``camera`` imaging ``scene``.

    This function runs the camera pipeline on ``scene`` and compares the
    rendered result to an ideal image using several existing quality metrics.
    The returned dictionary contains the following entries:

    ``"mtf"``
        Tuple ``(freqs, mtf)`` from :func:`camera_mtf`.
    ``"deltaE"``
        CIELAB color difference image between the ideal rendering and the
        camera result using :func:`~isetcam.metrics.delta_e_ab`.
    ``"vsnr"``
        Visible SNR value computed by :func:`camera_vsnr`.
    """

    # Compute the camera result for the scene
    camera = camera_compute(camera, scene)

    # Ideal XYZ image from the scene photon data
    energy = quanta_to_energy(scene.wave, scene.photons)
    xyz_ideal = ie_xyz_from_energy(energy, scene.wave)
    srgb_ideal, _, _ = xyz_to_srgb(xyz_ideal)
    lab_ideal = srgb_to_lab(srgb_ideal, _WHITEPOINT)

    # Approximate display rendering by normalizing the sensor response and
    # replicating it across RGB channels
    volts = camera.sensor.volts.astype(float)
    if volts.size == 0:
        raise ValueError("camera.sensor.volts is empty")
    scaled = volts / volts.max() if volts.max() > 0 else volts
    srgb_result = np.repeat(scaled[:, :, None], 3, axis=2)
    lab_result = srgb_to_lab(srgb_result, _WHITEPOINT)

    delta_e = delta_e_ab(lab_ideal, lab_result)

    freqs, mtf = camera_mtf(camera)
    vsnr_val = camera_vsnr(camera, scene)

    return {
        "mtf": (freqs, mtf),
        "deltaE": delta_e,
        "vsnr": vsnr_val,
    }


__all__ = ["camera_full_reference"]
