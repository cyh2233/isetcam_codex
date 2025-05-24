import numpy as np

from isetcam import (
    srgb_to_linear,
    linear_to_srgb,
    srgb_to_xyz,
    xyz_to_srgb,
)


# Expected white point of sRGB in XYZ (D65 with unit luminance)
_WHITE = np.array([0.9505, 1.0, 1.0890])


def _expected_srgb_to_xyz(srgb: np.ndarray) -> np.ndarray:
    M = np.array([
        [0.41238088, 0.21261986, 0.0193435],
        [0.35757284, 0.71513879, 0.11921217],
        [0.18045230, 0.07214994, 0.95050657],
    ])
    srgb = np.asarray(srgb)
    lrgb = srgb.copy()
    mask = lrgb > 0.04045
    lrgb[mask] = ((lrgb[mask] + 0.055) / 1.055) ** 2.4
    lrgb[~mask] = lrgb[~mask] / 12.92
    xw = lrgb.reshape(-1, 3)
    xyz = xw @ M
    return xyz.reshape(srgb.shape)


def _expected_xyz_to_srgb(xyz: np.ndarray):
    M = np.array([
        [3.2410, -0.9692, 0.0556],
        [-1.5374, 1.8760, -0.2040],
        [-0.4986, 0.0416, 1.0570],
    ])
    xyz = np.asarray(xyz, float)
    xw = xyz.reshape(-1, 3)
    maxY = xw[:, 1].max()
    if maxY > 1:
        xw = xw / maxY
    else:
        maxY = 1.0
    xw = np.clip(xw, 0.0, 1.0)
    lrgb = xw @ M
    clip = np.clip(lrgb, 0.0, 1.0)
    srgb = clip.copy()
    mask = srgb > 0.0031308
    srgb[mask] = 1.055 * srgb[mask] ** (1 / 2.4) - 0.055
    srgb[~mask] = srgb[~mask] * 12.92
    return srgb.reshape(xyz.shape), lrgb.reshape(xyz.shape), maxY


def test_white_point():
    xyz = srgb_to_xyz(np.ones((1, 1, 3)))
    assert np.allclose(xyz.reshape(3), _WHITE, atol=1e-4)


def test_srgb_linear_round_trip():
    srgb = np.random.rand(10, 3)
    lrgb = srgb_to_linear(srgb)
    srgb2 = linear_to_srgb(lrgb)
    assert np.allclose(srgb2, srgb, atol=1e-6)


def test_srgb_xyz_round_trip_rgb():
    srgb = np.random.rand(4, 5, 3)
    xyz = srgb_to_xyz(srgb)
    srgb2, lrgb, maxY = xyz_to_srgb(xyz)
    assert np.allclose(srgb2, srgb, atol=1e-6)
    assert maxY == 1.0
    assert lrgb.shape == srgb.shape


def test_xyz_scaling():
    xyz = 2 * _WHITE.reshape(1, 1, 3)
    srgb, lrgb, maxY = xyz_to_srgb(xyz)
    assert np.allclose(srgb, 1.0, atol=1e-4)
    assert np.isclose(maxY, 2.0)
    assert lrgb.shape == xyz.shape


def test_against_matlab_formula():
    srgb = np.random.rand(6, 3)
    xyz = srgb_to_xyz(srgb)
    expected = _expected_srgb_to_xyz(srgb)
    assert np.allclose(xyz, expected)

    srgb2, lrgb, maxY = xyz_to_srgb(xyz)
    ex_srgb, ex_lrgb, ex_maxY = _expected_xyz_to_srgb(xyz)
    assert np.allclose(srgb2, ex_srgb)
    assert np.allclose(lrgb, ex_lrgb)
    assert np.isclose(maxY, ex_maxY)
