# mypy: ignore-errors
"""Multivariate normal random number generator."""

from __future__ import annotations

import numpy as np


def ie_mvnrnd(mu: np.ndarray | float = 0.0, sigma: np.ndarray | float = 1.0, k: int | None = None) -> np.ndarray:
    """Draw samples from a multivariate normal distribution.

    Parameters
    ----------
    mu : array-like, optional
        Mean vector or array. When 1-D and ``k`` is provided, ``mu`` is
        replicated ``k`` times along the first axis.
    sigma : array-like, optional
        Covariance matrix. Must be square with size equal to the trailing
        dimension of ``mu``.
    k : int, optional
        Number of samples per row of ``mu`` when ``mu`` has a single row.

    Returns
    -------
    np.ndarray
        Samples drawn from ``N(mu, sigma)``.
    """
    mu = np.atleast_2d(np.asarray(mu, dtype=float))
    d = mu.shape[1]

    if k is not None and mu.shape[0] == 1:
        mu = np.tile(mu, (int(k), 1))

    sigma = np.asarray(sigma, dtype=float)
    if sigma.shape != (d, d):
        raise ValueError("sigma must be d x d matching columns of mu")

    try:
        u = np.linalg.cholesky(sigma)
    except np.linalg.LinAlgError:
        eigvals, eigvecs = np.linalg.eigh(sigma)
        if np.min(eigvals) < 0:
            raise ValueError("sigma must be positive semi-definite")
        u = eigvecs @ np.diag(np.sqrt(eigvals))

    rng = np.random.default_rng()
    z = rng.standard_normal(mu.shape)
    return z @ u.T + mu


__all__ = ["ie_mvnrnd"]
