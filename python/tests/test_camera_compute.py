import numpy as np
import pytest

from isetcam.camera import camera_create, camera_compute, Camera
from isetcam.scene import Scene
from isetcam.opticalimage import OpticalImage
from isetcam.sensor import Sensor


def _simple_scene(w: int = 2, h: int = 2, n_wave: int = 3) -> Scene:
    wave = np.arange(500, 500 + 10 * n_wave, 10)
    photons = np.arange(w * h * n_wave, dtype=float).reshape((h, w, n_wave))
    return Scene(photons=photons, wave=wave)


def test_camera_compute_from_scene():
    cam = camera_create()
    sc = _simple_scene()
    camera_compute(cam, sc)
    assert np.allclose(cam.optical_image.photons, sc.photons)
    expected = sc.photons.sum(axis=2) * cam.sensor.exposure_time
    assert np.allclose(cam.sensor.volts, expected)


def test_camera_compute_from_oi():
    cam = camera_create()
    sc = _simple_scene()
    oi = OpticalImage(photons=sc.photons.copy(), wave=sc.wave)
    camera_compute(cam, oi)
    expected = oi.photons.sum(axis=2) * cam.sensor.exposure_time
    assert np.allclose(cam.sensor.volts, expected)


def test_camera_compute_from_sensor():
    cam = camera_create()
    sc = _simple_scene()
    oi = OpticalImage(photons=sc.photons.copy(), wave=sc.wave)
    cam.optical_image = oi
    camera_compute(cam, "oi")
    volts = cam.sensor.volts.copy()
    new_sensor = Sensor(volts=np.zeros_like(volts), wave=sc.wave, exposure_time=cam.sensor.exposure_time)
    camera_compute(cam, new_sensor)
    assert cam.sensor is new_sensor
    camera_compute(cam, "sensor")
    # volts should remain unchanged when starting from 'sensor'
    assert np.allclose(cam.sensor.volts, new_sensor.volts)
