import numpy as np

from isetcam import ie_clip


def test_ie_clip_default():
    data = np.array([-1.0, 0.5, 2.0])
    out = ie_clip(data)
    assert np.allclose(out, [0.0, 0.5, 1.0])


def test_ie_clip_single_bound():
    data = np.array([-2.0, -0.3, 0.3, 1.2])
    out = ie_clip(data, 0.5)
    assert np.allclose(out, [-0.5, -0.3, 0.3, 0.5])


def test_ie_clip_two_bounds():
    data = np.array([-2.0, -0.5, 0.5, 2.0])
    out = ie_clip(data, -0.5, 1.5)
    assert np.allclose(out, [-0.5, -0.5, 0.5, 1.5])


def test_ie_clip_none_bound():
    data = np.array([-2.0, 1.0, 3.0])
    out = ie_clip(data, None, 2.0)
    assert np.allclose(out, [-2.0, 1.0, 2.0])
