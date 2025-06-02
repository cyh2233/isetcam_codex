# mypy: ignore-errors
"""Save an ISETCam session to disk."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict


def ie_save_session(session: Dict[str, Any], path: str | Path) -> None:
    """Serialize ``session`` to ``path`` in JSON format."""
    p = Path(path)
    with p.open("w", encoding="utf-8") as f:
        json.dump(session, f, indent=2)

