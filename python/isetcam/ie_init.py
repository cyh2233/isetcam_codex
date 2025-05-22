"""Session initialization utilities for ISETCam Python."""

from __future__ import annotations

import os
from datetime import datetime
from typing import Any, Dict
import warnings

try:
    import matplotlib.pyplot as plt
except Exception:  # pragma: no cover - matplotlib might not be installed
    plt = None  # type: ignore

# Global preferences and session storage
ISET_PREFS: Dict[str, Any] = {}
VC_SESSION: Dict[str, Any] = {}


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
        "init_clear": int(clear),
        "font_size": 12,
    })

    # Clear previous session data
    VC_SESSION.clear()

    # Initialize the session structure
    return ie_init_session()


def ie_init_session() -> Dict[str, Any]:
    """Initialize the global session structure.

    Returns
    -------
    Dict[str, Any]
        The newly created session dictionary stored in ``VC_SESSION``.
    """
    global VC_SESSION

    VC_SESSION = {
        "NAME": f"iset-{datetime.now():%Y%m%dT%H%M%S}",
        "DIR": os.getcwd(),
        "SELECTED": {
            "SCENE": None,
            "OPTICALIMAGE": None,
            "ISA": None,
            "VCIMAGE": None,
            "DISPLAY": None,
            "GRAPHWIN": None,
        },
        "SCENE": [None],
        "OPTICALIMAGE": [None],
        "ISA": [None],
        "VCIMAGE": [None],
        "GRAPHWIN": [],
        "DISPLAY": [None],
        "initHelp": 0,
        "GUI": {"waitbar": ISET_PREFS.get("waitbar", 0)},
    }
    return VC_SESSION
