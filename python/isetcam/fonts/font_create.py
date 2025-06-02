# mypy: ignore-errors
"""Create a :class:`Font` description."""

from __future__ import annotations

from .font_class import Font


def font_create(
    letter: str | None = None,
    family: str | None = None,
    size: int | None = None,
    dpi: int | None = None,
    style: str | None = None,
) -> Font:
    """Return a :class:`Font` instance."""
    if letter is None:
        letter = "g"
    if family is None:
        family = "DejaVuSans"
    if size is None:
        size = 14
    if dpi is None:
        dpi = 96
    if style is None:
        style = "NORMAL"
    f = Font(character=letter, family=family, size=size, dpi=dpi, style=style)
    return f


__all__ = ["font_create"]
