import numpy as np

from isetcam.sensor import Sensor, sensor_clear_data


def _simple_sensor() -> Sensor:
    volts = np.ones((2, 2), dtype=float)
    wave = np.array([500, 510])
    return Sensor(volts=volts, wave=wave, exposure_time=0.01)


def test_sensor_clear_data_removes_fields():
    s = _simple_sensor()
    s.offset_fpn_image = np.ones((2, 2))
    s.gain_fpn_image = np.ones((2, 2))
    s.data = object()
    s.crop_rect = (0, 0, 1, 1)
    s.full_size = (2, 2)

    out = sensor_clear_data(s)
    assert out is s
    for fld in [
        "offset_fpn_image",
        "gain_fpn_image",
        "data",
        "crop_rect",
        "full_size",
    ]:
        assert not hasattr(out, fld)


def test_sensor_clear_data_no_fields():
    s = _simple_sensor()
    out = sensor_clear_data(s)
    assert out is s
    assert np.array_equal(out.volts, s.volts)
    assert np.array_equal(out.wave, s.wave)
