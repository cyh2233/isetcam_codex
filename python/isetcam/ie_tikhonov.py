# mypy: ignore-errors
"""Solve a Tikhonov regularized least-squares problem."""

from __future__ import annotations

import numpy as np
from numpy.typing import ArrayLike


def ie_tikhonov(
    A: ArrayLike,
    b: ArrayLike,
    *,
    minnorm: float = 0.0,
    smoothness: float = 0.0,
) -> tuple[np.ndarray, np.ndarray]:
    """Solve ``A x \approx b`` using Tikhonov regularization.

    Parameters
    ----------
    A : array-like, shape (m, n)
        System matrix.
    b : array-like, shape (m,)
        Right-hand-side vector.
    minnorm : float, optional
        Weight for the minimum-norm term ``||x||^2``.
    smoothness : float, optional
        Weight for the smoothness term based on the second difference of ``x``.

    Returns
    -------
    tuple[np.ndarray, np.ndarray]
        ``x`` : Regularized solution.
        ``x_ols`` : Ordinary least-squares solution without regularization.
    """
    A = np.asarray(A, dtype=float)
    b = np.asarray(b, dtype=float).reshape(-1)

    m, n = A.shape
    if b.shape[0] != m:
        raise ValueError("b must have length matching rows of A")

    # Second-order finite difference matrix enforcing smoothness
    if smoothness != 0:
        D2 = np.diff(np.eye(n), 2, axis=0)
        reg_smooth = smoothness * (D2.T @ D2)
    else:
        reg_smooth = 0.0

    reg_min = minnorm * np.eye(n)

    lhs = A.T @ A + reg_min + reg_smooth
    rhs = A.T @ b

    x = np.linalg.solve(lhs, rhs)
    x_ols = np.linalg.lstsq(A, b, rcond=None)[0]
    return x, x_ols


__all__ = ["ie_tikhonov"]
