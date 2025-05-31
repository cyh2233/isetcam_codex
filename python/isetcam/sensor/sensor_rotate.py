"""Rotate the voltage data of a :class:`Sensor`."""

from __future__ import annotations

from scipy.ndimage import rotate as nd_rotate

from .sensor_class import Sensor


def sensor_rotate(sensor: Sensor, angle: float, fill: float = 0) -> Sensor:
    """Rotate ``sensor`` by ``angle`` degrees.

    Parameters
    ----------
    sensor : Sensor
        Input sensor to rotate.
    angle : float
        Rotation angle in degrees. Positive values rotate counter-clockwise.
    fill : float, optional
        Value used to fill areas created by the rotation. Defaults to ``0``.

    Returns
    -------
    Sensor
        New sensor containing the rotated voltage data with the same
        wavelength samples and name.
    """

    rotated = nd_rotate(
        sensor.volts,
        angle,
        axes=(1, 0),
        reshape=True,
        order=1,
        mode="constant",
        cval=float(fill),
    )
    return Sensor(
        volts=rotated,
        wave=sensor.wave,
        exposure_time=sensor.exposure_time,
        name=sensor.name,
    )
