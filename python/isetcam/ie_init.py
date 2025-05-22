"""Session initialization utilities for ISETCam Python."""

from __future__ import annotations

import os
from typing import Any, Dict
import warnings

try:
    import matplotlib.pyplot as plt
except Exception:  # pragma: no cover - matplotlib might not be installed
    plt = None  # type: ignore

# Import the session initialization routine and globals
from .ie_init_session import ie_init_session, vcSESSION, ISET_PREFS


def ie_init(clear: bool = False) -> Dict[str, Any]:
    """Initialize a fresh ISETCam session.

    Parameters
    ----------
    clear : bool, optional
        When ``True`` attempt to clear any existing session variables.

    Returns
    -------
    Dict[str, Any]
        The initialized session dictionary.
    """
    # Warn about known incompatibilities (mirrors MATLAB behavior)
    if "2019b" in os.sys.version:
        warnings.warn("Windows do not run correctly under version 2019b")

    # Close any open GUI windows
    if plt is not None:
        try:
            plt.close("all")
        except Exception:
            pass

    # Reset preferences to defaults
    ISET_PREFS.clear()
    ISET_PREFS.update({
        "waitbar": 0,
        "initClear": int(clear),
        "fontSize": 12,
    })

    # Clear previous session data
    vcSESSION.clear()

    # Initialize the session structure
    return ie_init_session()
