import numpy as np
from isetcam import vc_constants, energy_to_quanta


def test_energy_to_quanta():
    wave = np.array([500, 510, 520])
    energy = np.ones((3, 1))
    photons = energy_to_quanta(wave, energy)
    expected = (energy / (vc_constants('h') * vc_constants('c'))) * (
        1e-9 * wave[:, np.newaxis]
    )
    assert np.allclose(photons, expected)
