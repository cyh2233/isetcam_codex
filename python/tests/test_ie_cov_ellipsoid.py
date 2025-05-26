import numpy as np
import pytest

from isetcam import ie_cov_ellipsoid


def test_unit_sphere():
    cov = np.eye(3)
    X, Y, Z = ie_cov_ellipsoid(cov, n_points=10)
    r = X**2 + Y**2 + Z**2
    assert np.allclose(r, 1.0, atol=1e-6)


def test_scaled_shifted_ellipsoid():
    cov = np.diag([4.0, 9.0, 16.0])
    center = np.array([1.0, 2.0, 3.0])
    X, Y, Z = ie_cov_ellipsoid(cov, center=center, n_points=8)
    val = ((X - center[0]) ** 2) / 4 + ((Y - center[1]) ** 2) / 9 + ((Z - center[2]) ** 2) / 16
    assert np.allclose(val, 1.0, atol=1e-6)


def test_bad_shape():
    with pytest.raises(ValueError):
        ie_cov_ellipsoid(np.eye(2))

