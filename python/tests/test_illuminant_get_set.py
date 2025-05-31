import numpy as np

from isetcam.illuminant import Illuminant, illuminant_get, illuminant_set


def test_illuminant_get_set():
    wave = np.array([500, 510])
    spd = np.ones(2)
    illum = Illuminant(spd=spd.copy(), wave=wave, name="orig")

    assert np.allclose(illuminant_get(illum, " sPd"), spd)
    assert np.array_equal(illuminant_get(illum, "WAVE"), wave)
    assert illuminant_get(illum, "N WAVE") == 2
    assert illuminant_get(illum, " NAME ") == "orig"

    new_spd = np.zeros_like(spd)
    illuminant_set(illum, " Spd ", new_spd)
    assert np.allclose(illuminant_get(illum, "SPD"), new_spd)

    new_wave = np.array([400, 500, 600])
    illuminant_set(illum, "wave", new_wave)
    assert np.array_equal(illuminant_get(illum, "wave"), new_wave)
    assert illuminant_get(illum, "n_wave") == len(new_wave)

    illuminant_set(illum, "NAME", "new")
    assert illuminant_get(illum, "name") == "new"
