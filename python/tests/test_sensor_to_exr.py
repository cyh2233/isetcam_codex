import io
import numpy as np
import pytest

from isetcam.io import openexr_read
from isetcam.sensor import Sensor, sensor_to_exr


def _backend_available() -> bool:
    try:
        import OpenEXR  # noqa: F401
        return True
    except Exception:
        pass
    import imageio.v2 as iio
    try:
        with iio.get_writer(io.BytesIO(), format='EXR-FI'):
            pass
        return True
    except Exception:
        return False


@pytest.mark.skipif(not _backend_available(), reason="OpenEXR support not available")
def test_sensor_to_exr_roundtrip_rgb(tmp_path):
    volts = np.stack([
        np.full((2, 3), 0.1, dtype=np.float32),
        np.full((2, 3), 0.2, dtype=np.float32),
        np.full((2, 3), 0.3, dtype=np.float32),
    ], axis=2)
    s = Sensor(volts=volts, exposure_time=0.01, wave=np.array([550]))
    path = tmp_path / 'sensor.exr'
    sensor_to_exr(s, path)
    loaded = openexr_read(path)
    assert set(loaded.keys()) == {'R', 'G', 'B'}
    assert np.allclose(loaded['R'], volts[:, :, 0])
    assert np.allclose(loaded['G'], volts[:, :, 1])
    assert np.allclose(loaded['B'], volts[:, :, 2])


@pytest.mark.skipif(not _backend_available(), reason="OpenEXR support not available")
def test_sensor_to_exr_roundtrip_gray(tmp_path):
    volts = np.random.rand(3, 2).astype(np.float32)
    s = Sensor(volts=volts, exposure_time=0.01, wave=np.array([550]))
    path = tmp_path / 'sensor_gray.exr'
    sensor_to_exr(s, path)
    loaded = openexr_read(path)
    assert list(loaded.keys()) == ['Y']
    assert np.allclose(loaded['Y'], volts)
