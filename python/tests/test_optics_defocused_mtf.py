import numpy as np

from isetcam.optics import (
    Optics,
    optics_defocused_mtf,
    optics_defocus_core,
)


def test_optics_defocused_mtf_basic():
    s = np.linspace(0, 2, 5)
    alpha = np.zeros_like(s)
    out = optics_defocused_mtf(s, alpha)
    nf = np.abs(s) / 2.0
    beta = np.sqrt(1.0 - nf ** 2)
    expected = (2.0 / np.pi) * (np.arccos(nf) - nf * beta)
    expected /= expected[0]
    assert np.allclose(out, expected)


def test_optics_defocus_core_simple():
    optics = Optics(f_number=4.0, f_length=0.005, wave=np.array([500]))
    sample_sf = np.array([0.0, 10.0, 20.0])
    D = np.array([0.5])

    otf, sfmm = optics_defocus_core(optics, sample_sf, D)

    p = optics.f_length / (2.0 * optics.f_number)
    D0 = 1.0 / optics.f_length
    w20 = (p ** 2 / 2.0) * (D0 * D) / (D0 + D)
    c = D0 / np.tan(np.deg2rad(1.0))
    cSF = sample_sf * c
    cSF[0] = np.min(cSF[1:]) * 1e-12
    lam = optics.wave[0] * 1e-9
    s = (lam / (D0 * p)) * cSF
    alpha = (4.0 * np.pi / lam) * w20[0] * np.abs(s)
    expected_otf = optics_defocused_mtf(s, np.abs(alpha))

    deg_per_mm = 1.0 / (np.tan(np.deg2rad(1.0)) * (1.0 / D0) * 1000.0)
    expected_sfmm = sample_sf * deg_per_mm

    assert np.allclose(otf[0], expected_otf)
    assert np.allclose(sfmm, expected_sfmm)
