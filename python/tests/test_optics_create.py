import numpy as np

from isetcam.optics import optics_create, Optics


def test_optics_create_default():
    opt = optics_create()
    assert isinstance(opt, Optics)
    assert opt.f_number == 4.0
    assert opt.f_length == 0.004
    assert opt.transmittance.shape == opt.wave.shape


def test_optics_create_diffuser():
    opt = optics_create("diffuser", wave=np.array([500, 510]))
    assert np.allclose(opt.transmittance, 0.5)
    assert opt.wave.size == 2
