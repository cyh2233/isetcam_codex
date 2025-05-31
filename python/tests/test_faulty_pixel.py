import numpy as np

from isetcam.imgproc.demosaic.faulty_pixel import (
    faulty_insert,
    faulty_list,
    faulty_pixel_correction,
)


def test_faulty_list_spacing():
    lst = faulty_list(10, 10, n_bad_pixels=5, min_separation=2)
    assert lst.shape == (5, 2)
    for i in range(len(lst)):
        for j in range(i + 1, len(lst)):
            dist = np.hypot(*(lst[i] - lst[j]))
            assert dist >= 2


def test_faulty_insert_and_correction():
    pattern = "rggb"
    bayer = np.arange(36, dtype=float).reshape(6, 6)
    coords = np.array([[2, 2]])
    faulty = faulty_insert(coords, bayer, val=0)
    corrected = faulty_pixel_correction(coords, faulty, pattern, method="bilinear")
    expected = bayer.copy()
    expected[2, 2] = (bayer[0, 2] + bayer[4, 2] + bayer[2, 0] + bayer[2, 4]) / 4
    assert np.allclose(corrected, expected)
