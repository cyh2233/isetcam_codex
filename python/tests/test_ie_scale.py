import numpy as np

from isetcam import ie_scale, ie_scale_columns


def test_ie_scale_default():
    data = np.array([-1.0, 0.0, 1.0, 2.0])
    scaled, mn, mx = ie_scale(data)
    assert np.isclose(mn, -1.0)
    assert np.isclose(mx, 2.0)
    assert np.isclose(scaled.min(), 0.0)
    assert np.isclose(scaled.max(), 1.0)


def test_ie_scale_range():
    data = np.array([-5.0, 0.0, 5.0])
    scaled, mn, mx = ie_scale(data, -1.0, 1.0)
    assert np.isclose(mn, -5.0)
    assert np.isclose(mx, 5.0)
    assert np.allclose(scaled, [-1.0, 0.0, 1.0])


def test_ie_scale_columns():
    X = np.array([[1.0, 2.0], [2.0, 4.0]])
    out = ie_scale_columns(X)
    expected = np.array([[0.5, 0.5], [1.0, 1.0]])
    assert np.allclose(out, expected)
