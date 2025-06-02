import numpy as np

from isetcam.optics import Optics, optics_coc


def _expected(optics: Optics, focus: float, dist: np.ndarray) -> np.ndarray:
    A = optics.f_length / optics.f_number
    fO = 1.0 / ((1.0 / optics.f_length) - (1.0 / focus))
    fX = 1.0 / ((1.0 / optics.f_length) - (1.0 / dist))
    fX = np.maximum(fX, 0.0)
    return A * np.abs(fX - fO) / fX


def test_optics_coc_basic():
    opt = Optics(f_number=5.0, f_length=0.05)
    focus = 3.0
    dists = np.array([2.0, 3.0, 4.0])
    out = optics_coc(opt, focus, dists)
    exp = _expected(opt, focus, dists)
    assert np.allclose(out, exp)
    assert np.isclose(out[1], 0.0)


def test_optics_coc_units():
    opt = Optics(f_number=5.0, f_length=0.05)
    focus = 3.0
    d = 4.0
    out_m = optics_coc(opt, focus, d, units="m")
    out_mm = optics_coc(opt, focus, d, units="mm")
    assert np.allclose(out_mm, out_m * 1e3)
