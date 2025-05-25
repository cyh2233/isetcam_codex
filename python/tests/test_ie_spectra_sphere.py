import numpy as np

from isetcam import ie_spectra_sphere, ie_xyz_from_energy
from isetcam.illuminant import illuminant_blackbody


def test_ie_spectra_sphere_basic():
    wave = np.arange(400, 701, 10)
    base = illuminant_blackbody(6500, wave)
    spectra, xyz, xyz0, basis = ie_spectra_sphere(wave, base, n=4)

    n_samples = (4 + 1) * (4 + 1)
    assert spectra.shape == (len(wave), n_samples)
    assert xyz.shape == (n_samples, 3)
    assert xyz0.shape == (3,)
    assert basis.shape[0] == len(wave)

    expected0 = ie_xyz_from_energy(base[np.newaxis, :], wave)[0]
    assert np.allclose(xyz0, expected0)

    expected_xyz = ie_xyz_from_energy(spectra.T, wave)
    assert np.allclose(xyz, expected_xyz)

