import numpy as np

from isetcam import srgb_parameters, xyy_to_xyz


def test_srgb_parameters_all():
    params = srgb_parameters()
    expected = np.array([
        [0.6400, 0.3000, 0.1500, 0.3127],
        [0.3300, 0.6000, 0.0600, 0.3290],
        [0.2126, 0.7152, 0.0722, 1.0000],
    ])
    assert np.allclose(params, expected)


def test_srgb_parameters_subvalues():
    chroma = srgb_parameters("chromaticity")
    lum = srgb_parameters("luminance")
    xyY = srgb_parameters("xyywhite")
    xyz = srgb_parameters("XYZwhite")

    base = np.array([
        [0.6400, 0.3000, 0.1500, 0.3127],
        [0.3300, 0.6000, 0.0600, 0.3290],
        [0.2126, 0.7152, 0.0722, 1.0000],
    ])

    assert np.allclose(chroma, base[0:2, 0:3])
    assert np.allclose(lum, base[2, 0:3])
    assert np.allclose(xyY, base[:, 3])

    expected_xyz = xyy_to_xyz(xyY.reshape(1, 3)).reshape(3)
    assert np.allclose(xyz, expected_xyz)

