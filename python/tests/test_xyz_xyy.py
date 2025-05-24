import numpy as np

from isetcam import xyz_to_xyy, xyy_to_xyz


def _expected_xyz_to_xyy(xyz: np.ndarray) -> np.ndarray:
    xyz = np.asarray(xyz, float)
    s = xyz.sum(axis=-1)
    x = np.zeros_like(s)
    y = np.zeros_like(s)
    mask = s != 0
    x[mask] = xyz[..., 0][mask] / s[mask]
    y[mask] = xyz[..., 1][mask] / s[mask]
    Y = xyz[..., 1]
    return np.stack([x, y, Y], axis=-1)


def _expected_xyy_to_xyz(xyy: np.ndarray) -> np.ndarray:
    xyy = np.asarray(xyy, float)
    X = np.zeros_like(xyy[..., 0])
    Y = xyy[..., 2]
    Z = np.zeros_like(X)
    mask = xyy[..., 1] != 0
    X[mask] = (xyy[..., 0][mask] / xyy[..., 1][mask]) * Y[mask]
    sXYZ = np.zeros_like(X)
    sXYZ[mask] = Y[mask] / xyy[..., 1][mask]
    Z[mask] = sXYZ[mask] - Y[mask] - X[mask]
    return np.stack([X, Y, Z], axis=-1)


def test_xyz_xyy_round_trip_xw():
    xyz = np.random.rand(10, 3)
    xyY = xyz_to_xyy(xyz)
    xyz2 = xyy_to_xyz(xyY)
    assert np.allclose(xyz2, xyz, atol=1e-6)


def test_xyz_xyy_round_trip_rgb():
    xyz = np.random.rand(4, 5, 3)
    xyY = xyz_to_xyy(xyz)
    xyz2 = xyy_to_xyz(xyY)
    assert np.allclose(xyz2, xyz, atol=1e-6)


def test_xyz_xyy_formulas():
    xyz = np.random.rand(6, 3)
    xyY = xyz_to_xyy(xyz)
    expected_xyY = _expected_xyz_to_xyy(xyz)
    assert np.allclose(xyY, expected_xyY)

    xyz2 = xyy_to_xyz(xyY)
    expected_xyz = _expected_xyy_to_xyz(xyY)
    assert np.allclose(xyz2, expected_xyz)
