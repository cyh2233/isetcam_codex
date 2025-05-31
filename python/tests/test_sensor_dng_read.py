import numpy as np
import pytest

from isetcam.io import dng_write
from isetcam.sensor import Sensor, sensor_dng_read


def _backend_available() -> bool:
    try:
        import rawpy  # noqa: F401
        return True
    except Exception:
        return False


@pytest.mark.skipif(not _backend_available(), reason="rawpy not available")
def test_sensor_dng_read_roundtrip(tmp_path):
    data = (np.arange(12, dtype=np.uint16).reshape(3, 4) * 17) % 65535
    path = tmp_path / "test.dng"
    dng_write(path, data)
    sensor = sensor_dng_read(path)
    assert isinstance(sensor, Sensor)
    assert np.array_equal(sensor.volts.astype(np.uint16), data)
    assert isinstance(sensor.exposure_time, float)
