import numpy as np
import scipy.io
from dataclasses import asdict

from isetcam.sensor import Sensor, sensor_from_file


def test_sensor_from_file_roundtrip(tmp_path):
    s = Sensor(volts=np.array([[1.0, 2.0]]), exposure_time=0.05, wave=np.array([500, 600]), name="demo")
    path = tmp_path / "s.mat"
    scipy.io.savemat(path, {"sensor": asdict(s)})

    loaded = sensor_from_file(path)
    assert isinstance(loaded, Sensor)
    assert np.allclose(loaded.volts, s.volts)
    assert loaded.exposure_time == s.exposure_time
    assert np.array_equal(loaded.wave, s.wave)
    assert loaded.name == s.name


def test_sensor_from_file_isa(tmp_path):
    s = Sensor(volts=np.ones((2, 2)), exposure_time=0.1, wave=np.array([450, 550]), name="foo")
    path = tmp_path / "s.mat"
    scipy.io.savemat(path, {"isa": asdict(s)})
    loaded = sensor_from_file(path)
    assert np.allclose(loaded.volts, s.volts)
    assert loaded.name == s.name

