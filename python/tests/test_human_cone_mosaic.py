import numpy as np

from isetcam.human import human_cone_mosaic


def test_human_cone_mosaic_seed():
    sz = (3, 3)
    xy, cone_type, dens, seed = human_cone_mosaic(sz, r_seed=42)

    expected_xy = np.array([
        [-2.0, -2.0],
        [0.0, -2.0],
        [2.0, -2.0],
        [-2.0, 0.0],
        [0.0, 0.0],
        [2.0, 0.0],
        [-2.0, 2.0],
        [0.0, 2.0],
        [2.0, 2.0],
    ])
    expected_cone_type = np.array([
        [2, 1, 3],
        [2, 2, 3],
        [2, 2, 4],
    ])
    assert xy.shape == (9, 2)
    assert np.allclose(xy, expected_xy)
    assert np.array_equal(cone_type, expected_cone_type)
    assert np.isclose(dens.sum(), 1.0)
    # seed is a dict containing RNG state
    assert isinstance(seed, dict)
