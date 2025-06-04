import shutil
import pytest

from isetcam.scene import scene_from_pbrt


def _backend_available() -> bool:
    try:
        import iset3d  # noqa: F401
        return True
    except Exception:
        pass
    return shutil.which("pbrt") is not None


@pytest.mark.skipif(_backend_available(), reason="backend available")
def test_scene_from_pbrt_missing_dep():
    with pytest.raises(ImportError):
        scene_from_pbrt("dummy.pbrt")

