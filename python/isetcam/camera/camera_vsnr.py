"""Compute visible SNR for a camera scene pair."""

from __future__ import annotations

import numpy as np

from .camera_class import Camera
from ..scene import Scene
from ..opticalimage import OpticalImage
from ..sensor import sensor_compute
from ..quanta2energy import quanta_to_energy
from ..ie_xyz_from_energy import ie_xyz_from_energy
from ..metrics import xyz_to_vsnr


def camera_vsnr(camera: Camera, scene: Scene) -> float:
    """Return the VSNR value for ``camera`` imaging ``scene``.

    The scene is converted to an optical image which is passed through the
    sensor model using :func:`~isetcam.sensor.sensor_compute`. The scene
    spectral energy is converted to CIE XYZ by
    :func:`~isetcam.ie_xyz_from_energy` and the S-CIELAB domain variance is
    summarized with :func:`~isetcam.metrics.xyz_to_vsnr`.
    """

    # Create a trivial optical image from the scene
    oi = OpticalImage(photons=scene.photons, wave=scene.wave, name=scene.name)

    # Ensure sensor wavelengths match the scene
    if camera.sensor.wave is None or not np.array_equal(camera.sensor.wave, scene.wave):
        camera.sensor.wave = scene.wave.copy()
        if hasattr(camera.sensor, "qe"):
            camera.sensor.qe = np.ones_like(camera.sensor.wave, dtype=float)

    # Update the sensor response
    sensor_compute(camera.sensor, oi)

    # Convert scene photon data to energy and then to XYZ
    energy = quanta_to_energy(scene.wave, scene.photons)
    xyz = ie_xyz_from_energy(energy, scene.wave)

    white = np.array([1.0, 1.0, 1.0], dtype=float)
    return float(xyz_to_vsnr(xyz, white))


__all__ = ["camera_vsnr"]
