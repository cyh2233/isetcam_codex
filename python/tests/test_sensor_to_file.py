import numpy as np

from isetcam.sensor import Sensor, sensor_from_file, sensor_to_file


def test_sensor_to_file_roundtrip(tmp_path):
    s = Sensor(volts=np.array([[1.0, 2.0]]), exposure_time=0.05, wave=np.array([500, 600]), name="demo")
    path = tmp_path / "sensor.mat"
    sensor_to_file(s, path)

    loaded = sensor_from_file(path)
    assert isinstance(loaded, Sensor)
    assert np.allclose(loaded.volts, s.volts)
    assert loaded.exposure_time == s.exposure_time
    assert np.array_equal(loaded.wave, s.wave)
    assert loaded.name == s.name
