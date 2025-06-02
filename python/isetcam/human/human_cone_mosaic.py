# mypy: ignore-errors
"""Create a spatial arrangement of the human cone mosaic."""

from __future__ import annotations

import numpy as np


_DEF_DENSITIES = np.array([0.1, 0.55, 0.25, 0.1])


def _init_rng(r_seed):
    rng = np.random.default_rng()
    if r_seed is None:
        return rng, rng.bit_generator.state
    if isinstance(r_seed, (int, np.integer)):
        rng = np.random.default_rng(int(r_seed))
        return rng, rng.bit_generator.state
    rng.bit_generator.state = r_seed
    return rng, r_seed


def human_cone_mosaic(
    sz: tuple[int, int],
    densities: np.ndarray | None = None,
    um_cone_width: float = 2.0,
    r_seed=None,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, object]:
    """Return cone mosaic positions and types."""
    if densities is None:
        densities = _DEF_DENSITIES.copy()
    else:
        densities = np.asarray(densities, dtype=float)

    rng, seed_out = _init_rng(r_seed)

    s = densities.sum()
    if densities.size == 4:
        densities = densities / s
    elif densities.size == 3:
        if s >= 1:
            densities = np.hstack(([0.0], densities / s))
        else:
            densities = np.hstack(([1 - s], densities))
    n_types = 4

    n_locs = int(np.prod(sz))
    n_receptors = np.round(densities * n_locs).astype(int)
    if n_receptors.sum() < n_locs:
        i = int(np.argmax(n_receptors))
        n_receptors[i] += n_locs - n_receptors.sum()

    tmp = np.zeros(n_locs, dtype=int)
    start = 0
    for ii in range(n_types):
        tmp[start : start + n_receptors[ii]] = ii + 1
        start += n_receptors[ii]

    cone_type = rng.permutation(tmp).reshape(sz[0], sz[1])

    x = (np.arange(1, sz[1] + 1) * um_cone_width).astype(float)
    x -= x.mean()
    y = (np.arange(1, sz[0] + 1) * um_cone_width).astype(float)
    y -= y.mean()
    X, Y = np.meshgrid(x, y)
    xy = np.column_stack((X.ravel(), Y.ravel()))

    return xy, cone_type, densities, seed_out
