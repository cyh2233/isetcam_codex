import numpy as np
from isetcam import color_transform_matrix


def test_predefined_matrix():
    M = color_transform_matrix('xyz2srgb')
    expected = np.array([
        [3.2410, -0.9692, 0.0556],
        [-1.5374, 1.8760, -0.2040],
        [-0.4986, 0.0416, 1.0570],
    ])
    assert np.allclose(M, expected)


def test_least_squares_no_offset():
    src = np.array([[1.0, 0.0], [0.0, 1.0], [1.0, 1.0]])
    true_M = np.array([[1.0, 2.0, 3.0], [-1.0, 0.5, 0.0]])
    dst = src @ true_M
    M = color_transform_matrix(src=src, dst=dst)
    assert np.allclose(M, true_M)


def test_least_squares_offset():
    rng = np.random.RandomState(0)
    src = rng.rand(5, 2)
    true_M = np.array([[0.5, -1.0], [2.0, 0.0], [1.0, 1.0]])
    dst = np.hstack([src, np.ones((src.shape[0], 1))]) @ true_M
    M = color_transform_matrix(src=src, dst=dst, offset=True)
    assert np.allclose(M, true_M)
