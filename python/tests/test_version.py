import isetcam
import tomllib
from pathlib import Path


def test_version_matches_pyproject():
    pyproject = Path(__file__).resolve().parents[1] / "pyproject.toml"
    with open(pyproject, "rb") as f:
        data = tomllib.load(f)
    assert isetcam.__version__ == data["project"]["version"]
