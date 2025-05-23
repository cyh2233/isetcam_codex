import numpy as np
from isetcam import ie_luminance_to_radiance, luminance_from_energy


def test_luminance_match_default_wave():
    lum = 10.0
    peak = 360
    energy, wave = ie_luminance_to_radiance(lum, peak)
    calc = luminance_from_energy(energy, wave)
    assert np.isclose(calc, lum, atol=1e-6)
    assert len(energy) == len(wave)
    assert wave[0] == 300 and wave[-1] == 770


def test_custom_sd_and_wave():
    lum = 50.0
    peak = 425
    wave = np.arange(350, 701, 5)
    energy, out_wave = ie_luminance_to_radiance(lum, peak, sd=20, wave=wave)
    assert np.array_equal(out_wave, wave)
    calc = luminance_from_energy(energy, wave)
    assert np.isclose(calc, lum, atol=1e-6)
    # Energy should peak near the chosen wavelength
    idx = np.argmax(energy)
    assert abs(wave[idx] - peak) <= 5
