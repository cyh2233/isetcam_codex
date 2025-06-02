import numpy as np

from isetcam.ip import ip_demosaic


def test_ip_demosaic_default_bilinear():
    bayer = np.array([[1, 2], [3, 4]], dtype=float)
    expected = np.array(
        [
            [[1, 2.5, 4], [1, 2, 4]],
            [[1, 3, 4], [1, 2.5, 4]],
        ],
        dtype=float,
    )
    out = ip_demosaic(bayer, "rggb")
    assert np.allclose(out, expected)


def test_ip_demosaic_nearest():
    bayer = np.array([[1, 2], [3, 4]], dtype=float)
    expected = np.array(
        [
            [[1, 2, 4], [1, 2, 4]],
            [[1, 3, 4], [1, 3, 4]],
        ],
        dtype=float,
    )
    out = ip_demosaic(bayer, "rggb", method="nearest")
    assert np.array_equal(out, expected)


def test_ip_demosaic_shapes():
    bayer = np.arange(16, dtype=float).reshape(4, 4)
    for method in ["bilinear", "nearest", "adaptive", "pocs"]:
        out = ip_demosaic(bayer, "rggb", method=method)
        assert out.shape == (4, 4, 3)
