from importlib import util
from pathlib import Path
from typing import Any, Sequence


def _run_tutorial(script: str, argv: Sequence[str] | None = None) -> Any:
    """Execute a tutorial script located under ``python/tutorials/gui``."""

    base = Path(__file__).resolve().parents[3] / "tutorials" / "gui"
    path = base / f"{script}.py"
    spec = util.spec_from_file_location(script, path)
    mod = util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    if hasattr(mod, "main"):
        return mod.main(argv)
    return None
