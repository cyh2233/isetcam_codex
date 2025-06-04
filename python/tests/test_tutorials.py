import os
import sys
import subprocess
from pathlib import Path
import pytest

# Skip all tests in this module if matplotlib is unavailable
pytest.importorskip("matplotlib")

TUTORIALS = sorted(
    (Path(__file__).resolve().parents[1] / "tutorials").rglob("t_*.py")
)

@pytest.mark.parametrize("tutorial_path", TUTORIALS)
def test_run_tutorial(tutorial_path: Path) -> None:
    env = os.environ.copy()
    env["MPLBACKEND"] = "Agg"
    # Ensure the package can be imported when running in subprocess
    base = Path(__file__).resolve().parents[1]
    env["PYTHONPATH"] = str(base) + os.pathsep + env.get("PYTHONPATH", "")
    subprocess.run(
        [sys.executable, str(tutorial_path)],
        check=True,
        env=env,
        timeout=10,
    )

