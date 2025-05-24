import numpy as np

from isetcam.display import Display, display_apply_gamma


def _make_display(n_levels: int = 16) -> Display:
    wave = np.array([500, 510])
    spd = np.ones((2, 3))
    gamma = np.linspace(0, 1, n_levels).reshape(n_levels, 1).repeat(3, axis=1)
    return Display(spd=spd, wave=wave, gamma=gamma)


def test_display_apply_gamma_round_trip_xw():
    disp = _make_display()
    n_levels = disp.gamma.shape[0]
    dac = np.random.randint(0, n_levels, size=(10, 3)) / (n_levels - 1)
    lin = display_apply_gamma(dac, disp)
    dac2 = display_apply_gamma(lin, disp, inverse=True)
    assert np.allclose(dac2, dac, atol=1e-6)


def test_display_apply_gamma_round_trip_rgb():
    disp = _make_display()
    n_levels = disp.gamma.shape[0]
    dac = np.random.randint(0, n_levels, size=(4, 5, 3)) / (n_levels - 1)
    lin = display_apply_gamma(dac, disp)
    dac2 = display_apply_gamma(lin, disp, inverse=True)
    assert np.allclose(dac2, dac, atol=1e-6)
