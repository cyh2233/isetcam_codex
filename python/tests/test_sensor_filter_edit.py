import numpy as np
from scipy.io import loadmat

from isetcam.sensor import (
    Sensor,
    sensor_add_filter,
    sensor_delete_filter,
    sensor_replace_filter,
)
from isetcam import data_path


def _expected(path, wave):
    mat = loadmat(data_path(path), squeeze_me=True, struct_as_record=False)
    data = np.asarray(mat["data"], dtype=float).reshape(-1)
    src_wave = np.asarray(mat["wavelength"], dtype=float).reshape(-1)
    values = np.interp(wave, src_wave, data, left=0.0, right=0.0)
    name = str(np.atleast_1d(mat["filterNames"])[0])
    return values, name


def test_sensor_add_filter():
    wave = np.arange(370, 731, dtype=float)
    s = Sensor(volts=np.zeros((1, 1)), wave=wave, exposure_time=0.01)
    sensor_add_filter(s, data_path("sensor/colorfilters/B.mat"))
    expected, name = _expected("sensor/colorfilters/B.mat", wave)
    assert s.filter_spectra.shape == (wave.size, 1)
    assert np.allclose(s.filter_spectra[:, 0], expected)
    assert s.filter_names == [name]


def test_sensor_delete_filter():
    wave = np.arange(370, 731, dtype=float)
    s = Sensor(volts=np.zeros((1, 1)), wave=wave, exposure_time=0.01)
    sensor_add_filter(s, data_path("sensor/colorfilters/B.mat"))
    sensor_add_filter(s, data_path("sensor/colorfilters/G.mat"))
    sensor_delete_filter(s, 0)
    expected, name = _expected("sensor/colorfilters/G.mat", wave)
    assert s.filter_spectra.shape == (wave.size, 1)
    assert np.allclose(s.filter_spectra[:, 0], expected)
    assert s.filter_names == [name]


def test_sensor_replace_filter():
    wave = np.arange(370, 731, dtype=float)
    s = Sensor(volts=np.zeros((1, 1)), wave=wave, exposure_time=0.01)
    sensor_add_filter(s, data_path("sensor/colorfilters/B.mat"))
    sensor_add_filter(s, data_path("sensor/colorfilters/G.mat"))
    sensor_replace_filter(s, 1, data_path("sensor/colorfilters/R.mat"))
    expected_b, name_b = _expected("sensor/colorfilters/B.mat", wave)
    expected_r, name_r = _expected("sensor/colorfilters/R.mat", wave)
    assert s.filter_spectra.shape == (wave.size, 2)
    assert np.allclose(s.filter_spectra[:, 0], expected_b)
    assert np.allclose(s.filter_spectra[:, 1], expected_r)
    assert s.filter_names == [name_b, name_r]
