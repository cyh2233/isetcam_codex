import os
import subprocess
import sys


SCRIPTS = [
    "isetcam.tutorials.gui.t_roi_draw",
    "isetcam.tutorials.gui.t_gui_isetpref",
]


def _run(module: str) -> None:
    env = os.environ.copy()
    env["MPLBACKEND"] = "Agg"
    subprocess.run(
        [sys.executable, "-m", module, "--no-interactive"],
        check=True,
        env=env,
        timeout=5,
    )


def test_gui_scripts_launch():
    for mod in SCRIPTS:
        _run(mod)
