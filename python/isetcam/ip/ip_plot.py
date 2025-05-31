"""Basic IP plotting utilities."""

from __future__ import annotations

import numpy as np

try:  # pragma: no cover - matplotlib might not be installed
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle
except Exception:  # pragma: no cover - matplotlib might not be installed
    plt = None  # type: ignore
    Rectangle = None  # type: ignore

from .vcimage_class import VCImage
from ..ie_param_format import ie_param_format


_DEF_KINDS = {
    "horizontallineluminance",
    "verticallineluminance",
    "image",
    "imagewithgrid",
}


def _compute_luminance(rgb: np.ndarray) -> np.ndarray:
    coeffs = np.array([0.2126, 0.7152, 0.0722])
    return np.tensordot(rgb, coeffs, axes=([2], [0]))


def ip_plot(
    ip: VCImage,
    kind: str = "horizontallineluminance",
    loc: int | None = None,
    *,
    grid_spacing: int | None = None,
    roi: tuple[int, int, int, int] | None = None,
    ax: "plt.Axes | None" = None,
) -> "plt.Axes":
    """Plot properties of ``ip`` similar to MATLAB ``ipPlot``."""
    if plt is None:
        raise ImportError("matplotlib is required for ip_plot")

    key = ie_param_format(kind)
    if key not in _DEF_KINDS:
        raise ValueError(f"Unknown plot kind '{kind}'")

    rgb = np.asarray(ip.rgb, dtype=float)
    rows, cols = rgb.shape[:2]

    if key in {"horizontallineluminance", "verticallineluminance"}:
        lum = _compute_luminance(rgb)
        if key == "horizontallineluminance":
            r = rows // 2 if loc is None else int(loc)
            profile = lum[r, :]
            pos = np.arange(cols)
            xlabel = "Column index"
        else:
            c = cols // 2 if loc is None else int(loc)
            profile = lum[:, c]
            pos = np.arange(rows)
            xlabel = "Row index"
        if ax is None:
            fig, ax = plt.subplots()
        else:
            fig = ax.figure
        ax.plot(pos, profile, "b-")
        ax.set_xlabel(xlabel)
        ax.set_ylabel("Luminance (a.u.)")
        fig.tight_layout()
        return ax

    if ax is None:
        fig, ax = plt.subplots()
    else:
        fig = ax.figure
    img = np.clip(rgb, 0.0, 1.0)
    ax.imshow(img)
    ax.axis("off")

    if grid_spacing is not None:
        g = int(grid_spacing)
        for r in range(0, rows, g):
            ax.axhline(r - 0.5, color="k", linewidth=0.5)
        for c in range(0, cols, g):
            ax.axvline(c - 0.5, color="k", linewidth=0.5)
    if roi is not None and Rectangle is not None:
        r0, c0, h, w = [int(v) for v in roi]
        rect = Rectangle((c0, r0), w, h, edgecolor="y", facecolor="none", linewidth=1)
        ax.add_patch(rect)

    fig.tight_layout()
    return ax


__all__ = ["ip_plot"]
