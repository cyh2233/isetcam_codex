"""Normal probability density function."""

from __future__ import annotations

import numpy as np


def ie_normpdf(x: np.ndarray, mu: np.ndarray | float = 0.0, sigma: np.ndarray | float = 1.0) -> np.ndarray:
    """Return the normal probability density function evaluated at ``x``.

    Parameters
    ----------
    x : array-like
        Points at which to evaluate the pdf.
    mu : array-like or float, optional
        Mean of the distribution. Defaults to 0.
    sigma : array-like or float, optional
        Standard deviation of the distribution. Defaults to 1.

    Returns
    -------
    np.ndarray
        Values of the pdf evaluated at ``x``.
    """
    x = np.asarray(x, dtype=float)
    mu = np.asarray(mu, dtype=float)
    sigma = np.asarray(sigma, dtype=float)

    if np.any(sigma <= 0):
        raise ValueError("sigma must be > 0")

    xn = (x - mu) / sigma
    return np.exp(-0.5 * xn**2) / (np.sqrt(2 * np.pi) * sigma)


__all__ = ["ie_normpdf"]
