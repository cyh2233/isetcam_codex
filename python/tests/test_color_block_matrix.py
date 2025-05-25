import numpy as np

from isetcam import color_block_matrix


def test_default_block_matrix():
    wave = np.arange(400, 701, 10)
    M = color_block_matrix(wave)
    assert M.shape == (wave.size, 3)
    # Each column sums to 1
    assert np.allclose(M.sum(axis=0), 1.0)
    # Check regions
    assert np.allclose(M[:10, 2], 0.1)  # blue region
    assert np.allclose(M[10:18, 1], 1 / 8)  # green region
    assert np.allclose(M[18:, 0], 1 / 13)  # red region


def test_extrapolation():
    wave = np.array([350, 400, 500, 650, 750])
    M = color_block_matrix(wave, extrap_val=0.1)
    # matrix size
    assert M.shape == (wave.size, 3)
    assert np.allclose(M.sum(axis=0), 1.0)
    # extrapolated entries should be non-zero
    assert np.all(M[0] > 0)
    assert np.all(M[-1] > 0)
