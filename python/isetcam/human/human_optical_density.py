# mypy: ignore-errors
"""Default human optical density parameters."""

from __future__ import annotations

import numpy as np


_DEF_WAVE = np.arange(390, 731)


def human_optical_density(
    visual_field: str = "fovea", wave: np.ndarray | None = None
) -> dict:
    """Return default human optical density parameters."""
    if wave is None:
        wave = _DEF_WAVE.copy()
    else:
        wave = np.asarray(wave, dtype=float)

    visual_field = visual_field.lower()
    params: dict[str, float | str | np.ndarray] = {
        "visfield": visual_field,
        "wave": wave,
    }

    if visual_field in {"f", "fov", "fovea", "stf", "stockmanfovea"}:
        params.update(
            {
                "lens": 1.0,
                "macular": 0.28,
                "LPOD": 0.5,
                "MPOD": 0.5,
                "SPOD": 0.4,
                "melPOD": 0.5,
            }
        )
    elif visual_field in {
        "p",
        "peri",
        "periphery",
        "stp",
        "stockmanperi",
        "stockmanperiphery",
    }:
        params.update(
            {
                "lens": 1.0,
                "macular": 0.0,
                "LPOD": 0.38,
                "MPOD": 0.38,
                "SPOD": 0.3,
                "melPOD": 0.5,
            }
        )
    elif visual_field == "s1f":
        params.update(
            {
                "lens": 0.7467,
                "macular": 0.6910,
                "LPOD": 0.4964,
                "MPOD": 0.2250,
                "SPOD": 0.1480,
                "melPOD": 0.3239,
                "visfield": "f",
            }
        )
    elif visual_field == "s1p":
        params.update(
            {
                "lens": 0.7467,
                "macular": 0.0,
                "LPOD": 0.4964 / 0.5 * 0.38,
                "MPOD": 0.2250 / 0.5 * 0.38,
                "SPOD": 0.1480 / 0.4 * 0.3,
                "melPOD": 0.3239,
                "visfield": "p",
            }
        )
    elif visual_field == "s2f":
        params.update(
            {
                "lens": 0.7637,
                "macular": 0.5216,
                "LPOD": 0.4841,
                "MPOD": 0.2796,
                "SPOD": 0.2072,
                "melPOD": 0.3549,
                "visfield": "f",
            }
        )
    elif visual_field == "s2p":
        params.update(
            {
                "lens": 0.7637,
                "macular": 0.0,
                "LPOD": 0.4841 / 0.5 * 0.38,
                "MPOD": 0.2796 / 0.5 * 0.38,
                "SPOD": 0.2072 / 0.4 * 0.3,
                "melPOD": 0.3549,
                "visfield": "p",
            }
        )
    else:
        raise ValueError(f"Unknown visual field '{visual_field}'")

    return params
