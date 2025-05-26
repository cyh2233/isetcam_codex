import numpy as np

from isetcam import adobergb_parameters, xyy_to_xyz


def test_adobergb_parameters_all():
    params = adobergb_parameters()
    expected = np.array([
        [0.64, 0.21, 0.15, 0.3127],
        [0.33, 0.71, 0.06, 0.3290],
        [47.5744, 100.3776, 12.0320, 160.0],
    ])
    assert np.allclose(params, expected)


def test_adobergb_parameters_subvalues():
    chroma = adobergb_parameters("chromaticity")
    lum = adobergb_parameters("luminance")
    xyY = adobergb_parameters("xyywhite")
    xyz = adobergb_parameters("XYZwhite")

    base = np.array([
        [0.64, 0.21, 0.15, 0.3127],
        [0.33, 0.71, 0.06, 0.3290],
        [47.5744, 100.3776, 12.0320, 160.0],
    ])

    assert np.allclose(chroma, base[0:2, 0:3])
    assert np.allclose(lum, base[2, 0:3])
    assert np.allclose(xyY, base[:, 3])

    expected_xyz = xyy_to_xyz(xyY.reshape(1, 3)).reshape(3)
    assert np.allclose(xyz, expected_xyz)

