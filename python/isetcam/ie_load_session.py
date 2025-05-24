"""Load an ISETCam session from disk."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

from .ie_init_session import vcSESSION


def ie_load_session(path: str | Path) -> Dict[str, Any]:
    """Load session data from ``path`` and update ``vcSESSION``."""
    p = Path(path)
    with p.open("r", encoding="utf-8") as f:
        data = json.load(f)
    vcSESSION.clear()
    vcSESSION.update(data)
    return vcSESSION

