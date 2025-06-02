# mypy: ignore-errors
"""Format parameter names in ISET style."""

from __future__ import annotations

from typing import Any, Sequence
import numbers


def ie_param_format(value: Any) -> Any:
    """Convert parameter names to lowercase without spaces.

    Strings are normalized by converting to lowercase and removing any
    spaces. Lists and tuples are handled recursively such that every
    element at an even index (1-based odd position) is formatted using
    this rule. Numeric values and other data types are returned
    unchanged.

    Parameters
    ----------
    value : Any
        Value or container to be formatted.

    Returns
    -------
    Any
        Formatted value.
    """
    # Numbers just get returned unchanged
    if isinstance(value, numbers.Number):
        return value

    # Strings are converted to lowercase and spaces removed
    if isinstance(value, str):
        return value.replace(" ", "").lower()

    # Handle list or tuple of key/value pairs
    if isinstance(value, list):
        formatted = []
        for idx, item in enumerate(value):
            if idx % 2 == 0:
                formatted.append(ie_param_format(item))
            else:
                formatted.append(item)
        return formatted

    if isinstance(value, tuple):
        formatted = []
        for idx, item in enumerate(value):
            if idx % 2 == 0:
                formatted.append(ie_param_format(item))
            else:
                formatted.append(item)
        return tuple(formatted)

    # If it's some other sequence (but not a string), leave it as is
    return value
