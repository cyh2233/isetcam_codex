import numpy as np

from isetcam.io import pfm_read, pfm_write


def test_pfm_roundtrip_rgb(tmp_path):
    arr = np.random.rand(3, 4, 3).astype(np.float32)
    path = tmp_path / "rgb.pfm"
    pfm_write(path, arr)
    loaded = pfm_read(path)
    assert loaded.shape == arr.shape
    assert np.allclose(loaded, arr)


def test_pfm_roundtrip_single(tmp_path):
    arr = np.random.rand(2, 5).astype(np.float32)
    path = tmp_path / "gray.pfm"
    pfm_write(path, arr)
    loaded = pfm_read(path)
    assert loaded.shape == arr.shape
    assert np.allclose(loaded, arr)

