"""Display an RGB image using a ``Display`` definition."""

from __future__ import annotations

import numpy as np

try:
    import matplotlib.pyplot as plt
except Exception:  # pragma: no cover - matplotlib might not be installed
    plt = None  # type: ignore

from .display_class import Display
from .display_apply_gamma import display_apply_gamma


def display_show_image(image: np.ndarray, display: Display):
    """Render ``image`` for ``display`` and show with matplotlib.

    The input image is assumed to contain digital RGB drive values in
    ``[0, 1]``.  The display's gamma table is applied before showing the
    image.

    Parameters
    ----------
    image : np.ndarray
        RGB image in ``(R, C, 3)`` format.
    display : Display
        Display definition providing the gamma table.

    Returns
    -------
    matplotlib.axes.Axes
        The axis containing the displayed image.
    """
    if plt is None:
        raise ImportError("matplotlib is required for display_show_image")

    img = np.asarray(image, dtype=float)
    if display.gamma is not None:
        img = display_apply_gamma(img, display)

    fig, ax = plt.subplots()
    ax.imshow(np.clip(img, 0.0, 1.0))
    ax.axis("off")
    fig.tight_layout()
    return ax
