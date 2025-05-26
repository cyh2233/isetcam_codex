import numpy as np
import scipy.io
from dataclasses import asdict

from isetcam.camera import Camera, camera_from_file
from isetcam.sensor import Sensor
from isetcam.opticalimage import OpticalImage


def test_camera_from_file_roundtrip(tmp_path):
    sensor = Sensor(volts=np.ones((2, 2)), exposure_time=0.1, wave=np.array([500, 600]), name="s")
    oi = OpticalImage(photons=np.ones((2, 2, 2)), wave=np.array([500, 600]), name="oi")
    cam = Camera(sensor=sensor, optical_image=oi, name="cam")
    path = tmp_path / "cam.mat"
    scipy.io.savemat(path, {"camera": asdict(cam)})

    loaded = camera_from_file(path)
    assert isinstance(loaded, Camera)
    assert np.allclose(loaded.sensor.volts, sensor.volts)
    assert loaded.sensor.exposure_time == sensor.exposure_time
    assert np.array_equal(loaded.sensor.wave, sensor.wave)
    assert loaded.sensor.name == sensor.name
    assert np.allclose(loaded.optical_image.photons, oi.photons)
    assert np.array_equal(loaded.optical_image.wave, oi.wave)
    assert loaded.optical_image.name == oi.name
    assert loaded.name == cam.name


def test_camera_from_file_altvar(tmp_path):
    sensor = Sensor(volts=np.zeros((1, 1)), exposure_time=0.05, wave=np.array([500]), name="foo")
    oi = OpticalImage(photons=np.zeros((1, 1, 1)), wave=np.array([500]), name="bar")
    cam = Camera(sensor=sensor, optical_image=oi, name="baz")
    path = tmp_path / "cam.mat"
    scipy.io.savemat(path, {"cam": asdict(cam)})

    loaded = camera_from_file(path, candidate_vars=("camera", "cam"))
    assert loaded.name == cam.name
    assert np.allclose(loaded.sensor.volts, sensor.volts)
    assert np.allclose(loaded.optical_image.photons, oi.photons)
