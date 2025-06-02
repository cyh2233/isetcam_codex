# mypy: ignore-errors
"""Generate a short textual description of a :class:`Display`."""

from __future__ import annotations

import numpy as np

from .display_class import Display


ndefault = "No display structure"


def display_description(display: Display | None) -> str:
    """Return a multi-line description of ``display``."""
    if display is None:
        return ndefault

    lines: list[str] = []
    if display.name is not None:
        lines.append(f"Name:\t{display.name}")

    wave = np.asarray(display.wave, dtype=float)
    if wave.size:
        spacing = wave[1] - wave[0] if wave.size > 1 else 0
        lines.append(f"Wave:\t{int(wave[0])}:{int(spacing)}:{int(wave[-1])} nm")

    spd = np.asarray(display.spd)
    lines.append(f"# primaries:\t{spd.shape[1]}")

    if display.gamma is not None:
        n_levels = display.gamma.shape[0]
        bits = int(round(np.log2(n_levels)))
        lines.append(f"Color bit depth:\t{bits}")

    return "\n".join(lines) if lines else ndefault


__all__ = ["display_description"]
