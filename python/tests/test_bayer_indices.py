import numpy as np

from isetcam.imgproc.demosaic import bayer_indices


def test_bayer_indices_rggb():
    rx, ry, bx, by, g1x, g1y, g2x, g2y = bayer_indices("rggb", (4, 4))
    assert np.array_equal(rx, np.array([0, 2]))
    assert np.array_equal(ry, np.array([0, 2]))
    assert np.array_equal(bx, np.array([1, 3]))
    assert np.array_equal(by, np.array([1, 3]))
    assert np.array_equal(g1x, np.array([1, 3]))
    assert np.array_equal(g1y, np.array([0, 2]))
    assert np.array_equal(g2x, np.array([0, 2]))
    assert np.array_equal(g2y, np.array([1, 3]))


def test_bayer_indices_grbg():
    rx, ry, bx, by, g1x, g1y, g2x, g2y = bayer_indices("grbg", (4, 4))
    assert np.array_equal(rx, np.array([1, 3]))
    assert np.array_equal(ry, np.array([0, 2]))
    assert np.array_equal(bx, np.array([0, 2]))
    assert np.array_equal(by, np.array([1, 3]))
    assert np.array_equal(g1x, np.array([0, 2]))
    assert np.array_equal(g1y, np.array([0, 2]))
    assert np.array_equal(g2x, np.array([1, 3]))
    assert np.array_equal(g2y, np.array([1, 3]))


def test_bayer_indices_gbrg():
    rx, ry, bx, by, g1x, g1y, g2x, g2y = bayer_indices("gbrg", (4, 4))
    assert np.array_equal(rx, np.array([0, 2]))
    assert np.array_equal(ry, np.array([1, 3]))
    assert np.array_equal(bx, np.array([1, 3]))
    assert np.array_equal(by, np.array([0, 2]))
    assert np.array_equal(g1x, np.array([0, 2]))
    assert np.array_equal(g1y, np.array([0, 2]))
    assert np.array_equal(g2x, np.array([1, 3]))
    assert np.array_equal(g2y, np.array([1, 3]))


def test_bayer_indices_bggr():
    rx, ry, bx, by, g1x, g1y, g2x, g2y = bayer_indices("bggr", (4, 4))
    assert np.array_equal(rx, np.array([1, 3]))
    assert np.array_equal(ry, np.array([1, 3]))
    assert np.array_equal(bx, np.array([0, 2]))
    assert np.array_equal(by, np.array([0, 2]))
    assert np.array_equal(g1x, np.array([1, 3]))
    assert np.array_equal(g1y, np.array([0, 2]))
    assert np.array_equal(g2x, np.array([0, 2]))
    assert np.array_equal(g2y, np.array([1, 3]))
