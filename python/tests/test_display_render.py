import numpy as np
import matplotlib

matplotlib.use("Agg")

from isetcam.display import Display, display_apply_gamma, display_render
from isetcam.rgb_to_xw_format import rgb_to_xw_format
from isetcam.xw_to_rgb_format import xw_to_rgb_format


def _make_display(n_levels: int = 4) -> Display:
    wave = np.array([500, 510])
    spd = np.array([[1.0, 0.5, 0.2], [0.8, 0.3, 0.1]])
    gamma_vals = np.linspace(0, 1, n_levels) ** 2
    gamma = gamma_vals.reshape(n_levels, 1).repeat(3, axis=1)
    return Display(spd=spd, wave=wave, gamma=gamma)


def test_display_render_apply_gamma_xw():
    disp = _make_display()
    img = np.array(
        [
            [0.0, 0.5, 1.0],
            [0.25, 0.75, 0.1],
        ]
    )
    lin = display_apply_gamma(img, disp)
    expected = lin @ disp.spd.T
    out = display_render(img, disp, apply_gamma=True)
    assert np.allclose(out, expected)


def test_display_render_no_gamma_rgb():
    disp = _make_display()
    img = np.random.rand(2, 3, 3)
    expected_xw, rows, cols = rgb_to_xw_format(img)
    expected = expected_xw @ disp.spd.T
    expected = xw_to_rgb_format(expected, rows, cols)
    out = display_render(img, disp, apply_gamma=False)
    assert np.allclose(out, expected)


def test_display_render_apply_gamma_rgb():
    disp = _make_display()
    img = np.random.rand(3, 2, 3)
    lin = display_apply_gamma(img, disp)
    xw, rows, cols = rgb_to_xw_format(lin)
    expected = xw @ disp.spd.T
    expected = xw_to_rgb_format(expected, rows, cols)
    out = display_render(img, disp, apply_gamma=True)
    assert np.allclose(out, expected)
