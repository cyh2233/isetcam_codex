import numpy as np


def img_dead_leaves(patch_size: int = 256, noise_level: float = 0.0, seed: int | None = None) -> np.ndarray:
    """Return a grayscale dead-leaves test pattern.

    Parameters
    ----------
    patch_size: int
        Size in pixels of the square image.
    noise_level: float
        Standard deviation of optional additive Gaussian noise.
    seed: int, optional
        Seed for the random number generator for reproducibility.
    """
    rng = np.random.default_rng(seed)
    n = int(patch_size)

    sigma = 3.0
    rmin = 0.01
    rmax = 1.0
    nbr_iter = 5000

    img = np.full((n, n), np.inf, dtype=float)

    x = np.linspace(0.0, 1.0, n)
    Y, X = np.meshgrid(x, x)

    # radius distribution
    k = 200
    r_list = np.linspace(rmin, rmax, k)
    r_dist = 1.0 / (r_list ** sigma)
    if sigma > 0:
        r_dist = r_dist - 1.0 / (rmax ** sigma)
    r_dist = np.cumsum(r_dist)
    r_dist = (r_dist - r_dist.min()) / (r_dist.max() - r_dist.min())

    remaining = n * n
    for _ in range(nbr_iter):
        r = rng.random()
        idx = np.argmin(np.abs(r - r_dist))
        radius = r_list[idx]

        x0 = rng.random()
        y0 = rng.random()
        albedo = rng.random()

        mask = np.isinf(img) & ((X - x0) ** 2 + (Y - y0) ** 2 < radius ** 2)
        count = int(mask.sum())
        if count > 0:
            img[mask] = albedo
            remaining -= count
            if remaining <= 0:
                break

    img[np.isinf(img)] = 0.0

    if noise_level > 0:
        img += rng.normal(scale=float(noise_level), size=img.shape)
        img = np.clip(img, 0.0, 1.0)

    return img


__all__ = ["img_dead_leaves"]
