import numpy as np

from isetcam.optics import Optics, optics_dof


def test_optics_dof_basic():
    opt = Optics(f_number=4.0, f_length=0.05)
    o_dist = 2.0
    coc = 20e-6
    expected = 2.0 * opt.f_number * coc * (o_dist ** 2) / (opt.f_length ** 2)
    out = optics_dof(opt, o_dist, coc)
    assert np.isclose(out, expected)


def test_optics_dof_default_coc():
    opt = Optics(f_number=2.8, f_length=0.035)
    o_dist = 1.5
    expected = 2.0 * opt.f_number * 10e-6 * (o_dist ** 2) / (opt.f_length ** 2)
    out = optics_dof(opt, o_dist)
    assert np.isclose(out, expected)
