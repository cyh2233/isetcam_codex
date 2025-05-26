import io
import numpy as np
import pytest

from isetcam.io import openexr_read, openexr_write


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
def test_openexr_roundtrip_rgb(tmp_path):
    channels = {
        'R': np.full((4, 3), 0.1, dtype=np.float32),
        'G': np.full((4, 3), 0.2, dtype=np.float32),
        'B': np.full((4, 3), 0.3, dtype=np.float32),
    }
    path = tmp_path / 'rgb.exr'
    openexr_write(path, channels)
    loaded = openexr_read(path)
    assert set(loaded.keys()) == set(channels.keys())
    for k in channels:
        assert np.allclose(loaded[k], channels[k])


@pytest.mark.skipif(not _backend_available(), reason="OpenEXR support not available")
def test_openexr_roundtrip_single(tmp_path):
    channels = {'Y': np.random.rand(2, 2).astype(np.float32)}
    path = tmp_path / 'single.exr'
    openexr_write(path, channels)
    loaded = openexr_read(path)
    assert list(loaded.keys()) == ['Y']
    assert np.allclose(loaded['Y'], channels['Y'])
