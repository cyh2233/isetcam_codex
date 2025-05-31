import numpy as np
import pytest

from isetcam.io import dng_read, dng_write


def _backend_available() -> bool:
    try:
        import rawpy  # noqa: F401
        return True
    except Exception:
        return False


@pytest.mark.skipif(not _backend_available(), reason="rawpy not available")
def test_dng_roundtrip(tmp_path):
    data = (np.arange(12, dtype=np.uint16).reshape(3, 4) * 17) % 65535
    path = tmp_path / "test.dng"
    dng_write(path, data)
    loaded = dng_read(path)
    assert loaded.shape == data.shape
    assert np.all(loaded == data)
