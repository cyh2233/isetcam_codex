"""Generate spectral radiance from a monochromatic luminance value."""

from __future__ import annotations

import numpy as np

from .luminance_from_energy import luminance_from_energy


def ie_luminance_to_radiance(
    lum: float,
    peak_wave: float,
    sd: float = 10,
    wave: np.ndarray | None = None,
) -> tuple[np.ndarray, np.ndarray]:
    """Return spectral radiance matching ``lum`` for a Gaussian source.

    Parameters
    ----------
    lum : float
        Desired luminance of the source in candela per square meter.
    peak_wave : float
        Wavelength of the monochromatic peak in nanometers.  Valid range
        is roughly 350--720 nm.
    sd : float, optional
        Standard deviation of the Gaussian spectral model in nanometers.
    wave : array-like, optional
        Wavelength samples in nanometers.  When not provided, the range
        300--770 nm in 1 nm steps is used.

    Returns
    -------
    tuple[np.ndarray, np.ndarray]
        Radiance values in watts/sr/nm/m^2 and the wavelength samples.
    """
    if wave is None:
        wave = np.arange(300, 771, 1)
    wave = np.asarray(wave).reshape(-1)

    if not (350 <= peak_wave <= 720):
        raise ValueError("peak_wave must be between 350 and 720 nm")

    # Impulse at the peak wavelength
    energy = np.zeros_like(wave, dtype=float)
    idx = np.argmin(np.abs(wave - peak_wave))
    energy[idx] = 1.0

    # Gaussian kernel approximating MATLAB ``fspecial('gaussian',[8*sd,1],sd)``
    if len(wave) > 1:
        step = wave[1] - wave[0]
    else:
        step = 1
    size = max(int(round(8 * sd / step)), 1)
    if size % 2 == 0:
        size += 1
    rad = (size - 1) // 2
    x = np.arange(-rad, rad + 1) * step
    g = np.exp(-0.5 * (x / sd) ** 2)
    g /= g.sum()

    energy = np.convolve(energy, g, mode="same")

    # Scale to achieve the desired luminance
    lum_unit = luminance_from_energy(energy, wave)
    if lum_unit == 0:
        raise ValueError("Luminance of unit spectrum is zero; check wave range")
    energy *= lum / lum_unit

    # Verify luminance
    final_lum = luminance_from_energy(energy, wave)
    if not np.isclose(final_lum, lum, atol=1e-6):
        raise RuntimeError("Spectrum does not reproduce desired luminance")

    return energy, wave
