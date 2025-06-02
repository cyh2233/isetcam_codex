import numpy as np

from isetcam import ie_tone_curve, ie_apply_tone


def test_ie_tone_curve_properties():
    curve = ie_tone_curve(num_points=64)
    assert curve[0] >= 0 and curve[-1] <= 1
    assert np.all(np.diff(curve) >= 0)


def test_ie_apply_tone_identity():
    curve = np.linspace(0, 1, 32)
    img = np.random.rand(4, 4, 3)
    out = ie_apply_tone(img, curve)
    assert np.allclose(out, img, atol=0.05)


def test_ie_apply_tone_channels():
    curve = np.stack([np.linspace(0, 1, 16), np.linspace(0, 1, 16)**2], axis=1)
    img = np.random.rand(8, 2)
    out = ie_apply_tone(img, curve)
    assert out.shape == img.shape


