import numpy as np

from isetcam import (
    lms_to_xyz,
    xyz_to_lms,
    lms_to_srgb,
    srgb_to_lms,
)


_XYZ2LMS = np.array([
    [0.2689, 0.8518, -0.0358],
    [-0.3962, 1.1770, 0.1055],
    [0.0214, -0.0247, 0.5404],
])

_LMS2XYZ = np.array([
    [1.7910, -1.2884, 0.3702],
    [0.6068, 0.4097, -0.0398],
    [-0.0432, 0.0697, 1.8340],
])


def _expected_xyz_to_lms(xyz: np.ndarray) -> np.ndarray:
    xw = xyz.reshape(-1, 3)
    lms = xw @ _XYZ2LMS
    return lms.reshape(xyz.shape)


def _expected_lms_to_xyz(lms: np.ndarray) -> np.ndarray:
    xw = lms.reshape(-1, 3)
    xyz = xw @ _LMS2XYZ
    return xyz.reshape(lms.shape)


def test_xyz_lms_round_trip_rgb():
    xyz = np.random.rand(4, 5, 3)
    lms = xyz_to_lms(xyz)
    xyz2 = lms_to_xyz(lms)
    assert np.allclose(xyz2, xyz, atol=1e-4)


def test_xyz_lms_formulas():
    xyz = np.random.rand(6, 3)
    lms = xyz_to_lms(xyz)
    expected = _expected_xyz_to_lms(xyz)
    assert np.allclose(lms, expected)

    xyz2 = lms_to_xyz(lms)
    expected_xyz = _expected_lms_to_xyz(lms)
    assert np.allclose(xyz2, expected_xyz)


def test_srgb_lms_round_trip():
    srgb = np.random.rand(3, 4, 3)
    lms = srgb_to_lms(srgb)
    srgb2 = lms_to_srgb(lms)
    assert np.allclose(srgb2, srgb, atol=9e-4)
