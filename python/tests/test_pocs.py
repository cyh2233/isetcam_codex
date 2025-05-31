import numpy as np

from isetcam.imgproc import pocs
from isetcam.imgproc.demosaic.pocs import _bayer_masks


def test_pocs_preserves_samples():
    bayer = np.array([
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10, 11, 12],
        [13, 14, 15, 16],
    ], dtype=float)
    out = pocs(bayer, "rggb", iter_n=5)
    r_mask, _, b_mask = _bayer_masks("rggb", 4, 4)
    assert np.allclose(out[:, :, 0][r_mask], bayer[r_mask])
    assert np.allclose(out[:, :, 2][b_mask], bayer[b_mask])


def test_pocs_converges():
    bayer = np.array([
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10, 11, 12],
        [13, 14, 15, 16],
    ], dtype=float)
    out5 = pocs(bayer, "rggb", iter_n=5)
    out6 = pocs(bayer, "rggb", iter_n=6)
    diff = np.max(np.abs(out5 - out6))
    assert diff < 1e-5
