"""Convert spectral responsivity between energy and photon units."""

from __future__ import annotations

import numpy as np

from .energy_to_quanta import energy_to_quanta
from .quanta2energy import quanta_to_energy


def ie_responsivity_convert(
    responsivity: np.ndarray,
    wavelength: np.ndarray,
    method: str = "e2q",
) -> tuple[np.ndarray, np.ndarray]:
    """Convert responsivity curves between energy and quanta.

    Parameters
    ----------
    responsivity : np.ndarray
        Responsivity functions with wavelength along rows.
    wavelength : array-like
        Sampled wavelengths in nanometers.
    method : str, optional
        ``"e2q"`` converts energy-based responsivities for use with photon
        inputs. ``"q2e"`` converts the opposite way.

    Returns
    -------
    tuple of np.ndarray
        ``(converted, scale)`` where ``converted`` is the converted
        responsivity and ``scale`` is the per-wavelength scaling factor.
    """
    responsivity = np.asarray(responsivity, dtype=float)
    wavelength = np.asarray(wavelength).reshape(-1)

    if responsivity.shape[0] != len(wavelength):
        raise ValueError("wavelength length must match responsivity rows")

    method = method.lower()
    max_trans = responsivity.max()
    if method in {"e2q", "energy2quanta", "e2p", "energy2photons"}:
        s_factor = quanta_to_energy(wavelength, np.ones(len(wavelength))).reshape(-1)
    elif method in {"q2e", "quanta2energy", "p2e", "photons2energy"}:
        s_factor = energy_to_quanta(wavelength, np.ones(len(wavelength))).reshape(-1)
    else:
        raise ValueError("Unknown method")

    converted = s_factor[:, np.newaxis] * responsivity
    converted *= max_trans / converted.max()

    return converted, s_factor
