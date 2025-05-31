import numpy as np

from isetcam.imgproc import adaptive_laplacian


def test_adaptive_laplacian_rggb():
    bayer = np.array(
        [
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 12],
            [13, 14, 15, 16],
        ],
        dtype=float,
    )
    expected = np.array(
        [
            [[1.0625, 2.0, 2.625], [3.0, 3.75, 3.0], [3.5625, 4.0, 3.25], [3.0, 2.0, -1.75]],
            [[-0.1875, 3.5, 6.0], [6.125, 7.0, 7.875], [6.5625, 7.0, 8.0], [8.5, 7.0, 4.0]],
            [[4.5625, 10.0, 12.875], [11.0, 13.75, 13.25], [12.0625, 12.0, 12.5], [11.0, 6.0, 1.5]],
            [[-3.75, 5.0, 14.0], [5.8125, 15.0, 17.5], [5.8125, 15.0, 16.0], [7.75, 15.0, 8.0]],
        ],
        dtype=float,
    )
    out = adaptive_laplacian(bayer, "rggb")
    assert np.allclose(out, expected)


def test_adaptive_laplacian_bggr():
    bayer = np.array(
        [
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 12],
            [13, 14, 15, 16],
        ],
        dtype=float,
    )
    expected = np.array(
        [
            [[2.5, 5.0, 3.5], [6.0, 7.0, 4.0], [7.75, 7.0, 4.5], [8.0, 4.0, -2.75]],
            [[2.5, 9.0, 9.0], [9.0, 10.0, 10.0], [11.25, 11.0, 11.0], [15.0, 12.0, 5.75]],
            [[6.0, 13.0, 12.0], [14.0, 17.0, 13.5], [16.25, 15.0, 13.0], [16.0, 8.0, 3.75]],
            [[-3.25, 5.0, 9.0], [5.25, 10.0, 11.0], [9.0, 11.0, 11.0], [9.0, 12.0, 5.75]],
        ],
        dtype=float,
    )
    out = adaptive_laplacian(bayer, "bggr")
    assert np.allclose(out, expected)
