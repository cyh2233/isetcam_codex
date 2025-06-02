# mypy: ignore-errors
"""Simplified camera pipeline computation."""

from __future__ import annotations

from typing import Union

import numpy as np

from .camera_class import Camera
from ..sensor import Sensor, sensor_compute
from ..opticalimage import OpticalImage
from ..scene import Scene


def _scene_to_oi(scene: Scene) -> OpticalImage:
    """Convert ``scene`` to a trivial :class:`OpticalImage`.

    The current Python implementation does not model the effects of
    optics.  For now we simply copy the scene photon data into an optical
    image instance.
    """
    return OpticalImage(photons=scene.photons.copy(), wave=scene.wave, name=scene.name)


def _prepare_sensor(sensor: Sensor, wave: np.ndarray) -> Sensor:
    """Ensure ``sensor`` matches ``wave`` samples.

    If the sensor's wavelength sampling differs from ``wave`` the sensor's
    ``wave`` attribute is replaced with ``wave`` and its quantum efficiency
    (if present) resized to match.
    """
    if sensor.wave is None or not np.array_equal(sensor.wave, wave):
        sensor.wave = np.asarray(wave)
        if hasattr(sensor, "qe"):
            sensor.qe = np.ones_like(sensor.wave, dtype=float)
    return sensor


def camera_compute(camera: Camera, start: Union[str, Scene, OpticalImage, Sensor] = "sensor") -> Camera:  # noqa: E501
    """Run the basic camera pipeline.

    Parameters
    ----------
    camera:
        Camera object to update.
    start:
        Where to begin processing.  This can be a :class:`Scene`,
        :class:`OpticalImage`, :class:`Sensor` or one of the strings
        ``"scene"``, ``"oi"`` or ``"sensor"``.  The default is
        ``"sensor"`` which recomputes the sensor response from the
        camera's current optical image.

    Returns
    -------
    Camera
        ``camera`` with updated state.
    """

    # Determine the starting point
    if isinstance(start, Scene):
        oi = _scene_to_oi(start)
        camera.optical_image = oi
        camera.sensor = _prepare_sensor(camera.sensor, oi.wave)
        camera.sensor = sensor_compute(camera.sensor, oi)
        return camera

    if isinstance(start, OpticalImage):
        camera.optical_image = start
        camera.sensor = _prepare_sensor(camera.sensor, start.wave)
        camera.sensor = sensor_compute(camera.sensor, start)
        return camera

    if isinstance(start, Sensor):
        camera.sensor = _prepare_sensor(start, start.wave)
        # Nothing else to do
        return camera

    flag = str(start).lower().replace(" ", "") if isinstance(start, str) else None
    if flag is None:
        raise ValueError("Unsupported starting input for camera_compute")

    if flag == "scene":
        raise ValueError("Starting from 'scene' requires a Scene instance")
    if flag == "oi":
        camera.sensor = _prepare_sensor(camera.sensor, camera.optical_image.wave)
        camera.sensor = sensor_compute(camera.sensor, camera.optical_image)
        return camera
    if flag == "sensor":
        # Nothing to compute; return as-is
        return camera

    raise ValueError(f"Unknown starting flag '{start}'")
