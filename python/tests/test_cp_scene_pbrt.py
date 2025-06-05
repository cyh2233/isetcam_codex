import shutil
import numpy as np
import pytest

from isetcam.cp import CPScene
from isetcam.scene import Scene


def _backend_available() -> bool:
    try:
        import iset3d  # noqa: F401
        return True
    except Exception:
        pass
    return shutil.which("pbrt") is not None


@pytest.mark.skipif(not _backend_available(), reason="backend not available")
def test_cp_scene_render_pbrt(monkeypatch, tmp_path):
    pbrt_path = tmp_path / "test.pbrt"
    pbrt_path.write_text("Film \"image\" \"string filename\" [\"test.exr\"]")

    dest_root = tmp_path / "root"

    from isetcam import cp as cp_pkg
    monkeypatch.setattr(cp_pkg.cp_scene, "iset_root_path", lambda: dest_root)

    def fake_scene_from_pbrt(path):
        exr = path.with_suffix(".exr")
        exr.write_text("dummy")
        return Scene(photons=np.ones((1,1,1)), wave=np.array([550.0])), None, {}

    monkeypatch.setattr(cp_pkg.cp_scene, "scene_from_pbrt", fake_scene_from_pbrt)

    sc = CPScene(scene_type="pbrt", scene_path=str(pbrt_path))
    out = sc.render([0.1, 0.2])
    assert len(out) == 2

    comp = dest_root / "data" / "computed"
    files = sorted(comp.glob("test-*.exr"))
    assert len(files) == 2
