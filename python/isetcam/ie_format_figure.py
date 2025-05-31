"""Utility to format Matplotlib axes with ISETCam defaults."""

from __future__ import annotations

try:  # pragma: no cover - matplotlib might not be installed
    import matplotlib.pyplot as plt  # noqa: F401
except Exception:  # pragma: no cover - matplotlib might not be installed
    plt = None  # type: ignore


_IE_FIGURE_DEFAULTS: dict[str, object] = {
    "font_size": 10,
    "grid": False,
}


def set_ie_figure_defaults(**kwargs: object) -> None:
    """Update default formatting parameters.

    Parameters
    ----------
    **kwargs : dict
        ``font_size`` and ``grid`` can be updated.
    """
    for key in kwargs:
        if key not in _IE_FIGURE_DEFAULTS:
            raise KeyError(f"Unknown default '{key}'")
    _IE_FIGURE_DEFAULTS.update(kwargs)


def ie_format_figure(
    ax: "plt.Axes",
    *,
    xlabel: str | None = None,
    ylabel: str | None = None,
    font_size: int | None = None,
    grid: bool | None = None,
) -> "plt.Axes":
    """Apply ISETCam formatting to ``ax``.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        Axis to format.
    xlabel, ylabel : str, optional
        Axis label strings. When ``None`` existing labels are kept.
    font_size : int, optional
        Font size for labels and tick marks. Uses default when ``None``.
    grid : bool, optional
        Toggle grid visibility. Uses default when ``None``.

    Returns
    -------
    matplotlib.axes.Axes
        The formatted axis.
    """
    if plt is None:
        raise ImportError("matplotlib is required for ie_format_figure")

    fs = _IE_FIGURE_DEFAULTS["font_size"] if font_size is None else font_size
    gr = _IE_FIGURE_DEFAULTS["grid"] if grid is None else grid

    if xlabel is not None:
        ax.set_xlabel(xlabel)
    if ylabel is not None:
        ax.set_ylabel(ylabel)

    # Apply font sizes
    ax.xaxis.label.set_size(fs)
    ax.yaxis.label.set_size(fs)
    ax.title.set_size(fs)
    ax.tick_params(axis="both", labelsize=fs)

    ax.grid(gr)
    ax.figure.tight_layout()
    return ax


__all__ = ["ie_format_figure", "set_ie_figure_defaults", "_IE_FIGURE_DEFAULTS"]
