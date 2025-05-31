import numpy as np

from isetcam.optics import optics_psf, optics_otf


def _gaussian_psf(size: int, sigma: float) -> np.ndarray:
    ax = np.linspace(-(size // 2), size // 2, size)
    xx, yy = np.meshgrid(ax, ax)
    psf = np.exp(-(xx ** 2 + yy ** 2) / (2 * sigma ** 2))
    psf /= psf.sum()
    return psf


def test_psf_otf_roundtrip():
    psf = _gaussian_psf(32, 3.0)
    otf = optics_psf(psf)
    recon = optics_otf(otf)
    assert np.allclose(recon, psf, atol=1e-12)
    assert np.isclose(np.real(otf[0, 0]), 1.0, atol=1e-12)
