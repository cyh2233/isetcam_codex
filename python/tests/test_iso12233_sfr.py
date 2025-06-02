import numpy as np
import pytest

from isetcam.metrics import iso12233_sfr


def _slanted_edge(height=32, width=32, slope=0.2):
    x, y = np.meshgrid(np.arange(width), np.arange(height))
    edge = slope * y + width / 4
    return (x >= edge).astype(float)


def test_iso12233_sfr_shape_and_decreasing():
    img = _slanted_edge(40, 40, 0.1)
    freq, mtf = iso12233_sfr(img, delta_x=1)
    assert freq.shape == mtf.shape
    assert freq[0] == 0
    assert mtf[0] == pytest.approx(1.0)
    assert np.all(np.diff(freq) > 0)
    assert np.all(mtf >= 0)


def test_iso12233_sfr_color_matches_gray():
    img = _slanted_edge(32, 32, 0.1)
    color = np.stack([img, img, img], axis=-1)
    f1, m1 = iso12233_sfr(img, delta_x=1)
    f2, m2 = iso12233_sfr(color, delta_x=1)
    assert np.allclose(f1, f2)
    assert np.allclose(m1, m2)
