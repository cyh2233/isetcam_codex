import numpy as np
import pytest

from isetcam.sensor import sensor_create, Sensor


def test_sensor_create_default():
    s = sensor_create()
    assert isinstance(s, Sensor)
    assert s.exposure_time == 0.01
    assert hasattr(s, "qe")
    assert hasattr(s, "pixel_size")
    assert s.qe.size == s.wave.size
    assert s.filter_color_letters == "grbg"
    assert s.n_colors == 3


def test_sensor_create_custom_wave():
    wave = np.array([500, 510, 520])
    s = sensor_create(wave=wave)
    assert np.array_equal(s.wave, wave)
    assert s.qe.size == wave.size


@pytest.mark.parametrize(
    "kind,letters",
    [
        ("bayer (gbrg)", "gbrg"),
        ("bayer (rggb)", "rggb"),
        ("bayer (bggr)", "bggr"),
        ("bayer (grbg)", "grbg"),
    ],
)
def test_sensor_create_patterns(kind, letters):
    s = sensor_create(kind)
    assert s.filter_color_letters == letters
    assert s.n_colors == 3
