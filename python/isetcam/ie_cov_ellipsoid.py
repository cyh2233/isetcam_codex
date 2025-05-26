"""Generate ellipsoid coordinates from a covariance matrix."""

from __future__ import annotations

import numpy as np
from numpy.linalg import eigh


def ie_cov_ellipsoid(
    cov: np.ndarray, center: np.ndarray | None = None, n_points: int = 20
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return ``(X, Y, Z)`` points forming the ellipsoid described by ``cov``.

    The function computes a surface corresponding to one standard deviation
    of a multivariate normal distribution with covariance ``cov``.  The points
    can be visualized using ``matplotlib``::

        X, Y, Z = ie_cov_ellipsoid(cov)
        fig = plt.figure()
        ax = fig.add_subplot(111, projection="3d")
        ax.plot_surface(X, Y, Z, rstride=1, cstride=1, alpha=0.3)

    Parameters
    ----------
    cov : array-like of shape (3, 3)
        Covariance matrix defining the ellipsoid axes and orientation.
    center : array-like of length 3, optional
        Center of the ellipsoid.  Defaults to the origin.
    n_points : int, optional
        Number of sample points along each angular dimension of the unit
        sphere. Higher values yield a finer mesh.

    Returns
    -------
    tuple[np.ndarray, np.ndarray, np.ndarray]
        Arrays ``(X, Y, Z)`` with shape ``(n_points, n_points)`` describing the
        ellipsoid surface.
    """
    cov = np.asarray(cov, dtype=float)
    if cov.shape != (3, 3):
        raise ValueError("cov must be a 3x3 matrix")
    if center is None:
        center = np.zeros(3, dtype=float)
    else:
        center = np.asarray(center, dtype=float).reshape(3)

    # Eigen-decomposition of the covariance matrix
    eigvals, eigvecs = eigh(cov)
    if np.any(eigvals < 0):
        raise ValueError("covariance matrix must be positive semi-definite")
    radii = np.sqrt(eigvals)

    # Points on a unit sphere
    phi = np.linspace(0.0, 2 * np.pi, n_points)
    theta = np.linspace(0.0, np.pi, n_points)
    x = np.outer(np.cos(phi), np.sin(theta))
    y = np.outer(np.sin(phi), np.sin(theta))
    z = np.outer(np.ones_like(phi), np.cos(theta))
    sphere = np.stack((x, y, z), axis=-1)

    # Transform unit sphere to the ellipsoid
    transform = eigvecs @ np.diag(radii)
    pts = sphere.reshape(-1, 3).T
    ellipsoid = transform @ pts
    ellipsoid += center[:, None]
    ellipsoid = ellipsoid.T.reshape(n_points, n_points, 3)
    X = ellipsoid[:, :, 0]
    Y = ellipsoid[:, :, 1]
    Z = ellipsoid[:, :, 2]
    return X, Y, Z
