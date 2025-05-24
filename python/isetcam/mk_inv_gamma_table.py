"""Generate an inverse gamma lookup table."""

from __future__ import annotations

import numpy as np
import warnings


def mk_inv_gamma_table(
    gamma_table: np.ndarray, num_entries: int | None = None
) -> np.ndarray:
    """Compute inverse gamma mapping from intensity to digital levels.

    Parameters
    ----------
    gamma_table : array-like
        Gamma table mapping digital levels to linear intensity. Can be a
        1-D or 2-D array.
    num_entries : int, optional
        Number of entries in the inverse table. Defaults to
        ``4 * len(gamma_table)``.

    Returns
    -------
    np.ndarray
        Inverse gamma table with ``num_entries`` rows and the same number of
        columns as ``gamma_table``.
    """
    gamma = np.asarray(gamma_table, dtype=float)
    orig_shape = gamma.shape
    if gamma.ndim == 1:
        gamma = gamma.reshape(-1, 1)

    n_rows, n_cols = gamma.shape
    if num_entries is None:
        num_entries = 4 * n_rows

    inv = np.empty((num_entries, n_cols), dtype=float)
    query = np.linspace(0, 1, num_entries)

    for col in range(n_cols):
        tbl = gamma[:, col]
        if np.any(np.diff(tbl) <= 0):
            warnings.warn(
                f"Gamma table {col} NOT MONOTONIC. We are adjusting.",
                UserWarning,
            )
            tbl = np.sort(tbl)
            pos = np.where(np.diff(tbl) > 0)[0] + 1
            pos = np.insert(pos, 0, 0)
            mon_table = tbl[pos]
        else:
            mon_table = tbl
            pos = np.arange(len(tbl))

        inv[:, col] = np.interp(query, mon_table, pos)

    if orig_shape == (n_rows,):
        return inv[:, 0]
    return inv
