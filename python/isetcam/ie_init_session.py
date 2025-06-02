# mypy: ignore-errors
"""Initialize the ISETCam session structure (Python version)."""

from __future__ import annotations

import os
from datetime import datetime
from typing import Any, Dict

# Global preferences and session data
vcSESSION: Dict[str, Any] = {}
ISET_PREFS: Dict[str, Any] = {
    "waitbar": 0,
    "initClear": 0,
    "fontSize": 12,
}


def ie_init_session() -> Dict[str, Any]:
    """Create and return a new session dictionary.

    This function mirrors the behaviour of MATLAB's ``ieInitSession`` by
    initializing the global ``vcSESSION`` structure and returning it.
    """
    global vcSESSION

    vcSESSION = {
        "NAME": f"iset-{datetime.now():%Y%m%dT%H%M%S}",
        "DIR": os.getcwd(),
        "SELECTED": {
            "SCENE": [],
            "OPTICALIMAGE": [],
            "ISA": [],
            "VCIMAGE": [],
            "DISPLAY": [],
            "GRAPHWIN": [],
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
    return vcSESSION
