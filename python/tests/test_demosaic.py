import numpy as np

from isetcam.imgproc import ie_nearest_neighbor, ie_bilinear


def test_nearest_neighbor_rggb():
    bayer = np.array([[1, 2], [3, 4]], dtype=float)
    expected = np.array([
        [[1, 2, 4], [1, 2, 4]],
        [[1, 3, 4], [1, 3, 4]],
    ], dtype=float)
    out = ie_nearest_neighbor(bayer, "rggb")
    assert np.array_equal(out, expected)


def test_bilinear_rggb():
    bayer = np.array([[1, 2], [3, 4]], dtype=float)
    expected = np.array([
        [[1, 2.5, 4], [1, 2, 4]],
        [[1, 3, 4], [1, 2.5, 4]],
    ], dtype=float)
    out = ie_bilinear(bayer, "rggb")
    assert np.allclose(out, expected)
