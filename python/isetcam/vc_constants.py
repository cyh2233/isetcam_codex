# mypy: ignore-errors
"""Utility functions providing physical constants used across ISETCam."""

def vc_constants(name: str) -> float:
    """Return value of a named physical constant.

    Parameters
    ----------
    name : str
        Name of the constant. Supported values are ``'planck'``, ``'h'``,
        ``'plancksconstant'``, ``'q'`` (electron charge), ``'c'`` (speed of
        light), ``'j'`` (Boltzmann constant), and ``'mmPerDeg``.

    Returns
    -------
    float
        Numeric value of the requested constant.

    Raises
    ------
    KeyError
        If an unknown constant name is supplied.
    """
    key = name.lower()
    if key in {'planck', 'h', 'plancksconstant'}:
        return 6.626176e-34
    if key in {'q', 'electroncharge'}:
        return 1.602177e-19
    if key in {'c', 'speedoflight'}:
        return 2.99792458e8
    if key in {'j', 'joulesperkelvin', 'boltzman'}:
        return 1.380662e-23
    if key == 'mmperdeg':
        return 0.3
    raise KeyError(f"Unknown physical constant '{name}'")
