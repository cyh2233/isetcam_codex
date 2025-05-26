import numpy as np

from isetcam.optics import Optics, optics_get, optics_set


def test_optics_get_set():
    wave = np.array([500, 510, 520])
    trans = np.array([1.0, 0.9, 0.8])
    opt = Optics(f_number=4.0, f_length=0.004, wave=wave, transmittance=trans.copy(), name="orig")

    assert optics_get(opt, "f_number") == 4.0
    assert optics_get(opt, "f Length") == 0.004
    assert np.array_equal(optics_get(opt, "wave"), wave)
    assert optics_get(opt, "n wave") == 3
    assert np.allclose(optics_get(opt, "transmittance"), trans)
    assert optics_get(opt, "NaMe") == "orig"

    optics_set(opt, "f_number", 2.8)
    assert optics_get(opt, "fnumber") == 2.8

    optics_set(opt, "f_length", 0.005)
    assert optics_get(opt, "flength") == 0.005

    new_wave = np.array([600, 610])
    optics_set(opt, "wave", new_wave)
    assert np.array_equal(optics_get(opt, "wave"), new_wave)
    assert optics_get(opt, "n_wave") == len(new_wave)

    new_trans = np.array([0.5, 0.4])
    optics_set(opt, "transmittance", new_trans)
    assert np.allclose(optics_get(opt, "transmittance"), new_trans)

    optics_set(opt, "name", "new")
    assert optics_get(opt, "name") == "new"
