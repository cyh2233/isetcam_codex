"""Poisson random number generator with ISETCam options."""

from __future__ import annotations

import numpy as np
from numpy.random import Generator


_DEF_SEED = 1


def _make_rng(noise_flag: str, seed: int) -> tuple[Generator, int]:
    """Return a random generator according to ``noise_flag``.

    Parameters
    ----------
    noise_flag : {'random', 'frozen', 'donotset'}
        How the random generator seed should be handled.
    seed : int
        Seed value when ``noise_flag`` is 'frozen'.  When ``noise_flag`` is
        'random', a random seed is generated and returned.

    Returns
    -------
    tuple
        ``(rng, seed)`` where ``rng`` is a :class:`numpy.random.Generator` and
        ``seed`` is the seed actually used.
    """
    noise_flag = noise_flag.lower()
    if noise_flag == "frozen":
        return np.random.default_rng(seed), seed
    if noise_flag == "random":
        seed = np.random.SeedSequence().entropy % (2**32)
        return np.random.default_rng(int(seed)), int(seed)
    if noise_flag == "donotset":
        return np.random.default_rng(), seed
    raise ValueError("noise_flag must be 'random', 'frozen' or 'donotset'")


def ie_poisson(
    lam: np.ndarray | float,
    *,
    n_samp: int = 1,
    noise_flag: str = "random",
    seed: int = _DEF_SEED,
) -> tuple[np.ndarray, int]:
    """Generate Poisson-distributed random values.

    Parameters
    ----------
    lam : array-like or float
        Mean rate parameter(s) of the distribution.
    n_samp : int, optional
        Number of samples when ``lam`` is scalar. Ignored otherwise.
    noise_flag : {'random', 'frozen', 'donotset'}, optional
        Controls the random generator seed. ``'frozen'`` uses the supplied
        ``seed`` and returns it; ``'random'`` chooses a new random seed and
        returns it; ``'donotset'`` leaves the generator state unspecified.
    seed : int, optional
        Seed value used when ``noise_flag`` is ``'frozen'``.

    Returns
    -------
    tuple of np.ndarray and int
        ``(samples, seed)`` where ``samples`` contains the Poisson random
        values and ``seed`` is the seed used for generation.
    """
    lam = np.asarray(lam, dtype=float)

    rng, seed = _make_rng(noise_flag, int(seed))

    if lam.size == 1:
        val = rng.poisson(float(lam), size=(int(n_samp), int(n_samp)))
    else:
        val = rng.poisson(lam)

    return val, seed


__all__ = ["ie_poisson"]
