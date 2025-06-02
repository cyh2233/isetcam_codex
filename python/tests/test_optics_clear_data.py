import numpy as np

from isetcam.optics import Optics, optics_clear_data


def _simple_optics() -> Optics:
    wave = np.array([500, 510])
    return Optics(f_number=4.0, f_length=0.005, wave=wave)


def test_optics_clear_data_removes_fields():
    opt = _simple_optics()
    opt.otf_data = np.ones((2, 2), dtype=float)
    opt.cos4th_data = np.ones(5, dtype=float)

    out = optics_clear_data(opt)
    assert out is opt
    for fld in ["otf_data", "cos4th_data"]:
        assert not hasattr(out, fld)


def test_optics_clear_data_no_fields():
    opt = _simple_optics()
    out = optics_clear_data(opt)
    assert out is opt
    assert np.isclose(out.f_number, opt.f_number)
    assert np.isclose(out.f_length, opt.f_length)
    assert np.array_equal(out.wave, opt.wave)
    assert np.allclose(out.transmittance, opt.transmittance)
