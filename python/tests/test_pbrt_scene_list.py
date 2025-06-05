import pytest

from isetcam.scene import pbrt_scene_list


def _iset3d_available() -> bool:
    try:
        import iset3d  # noqa: F401
        return True
    except Exception:
        return False


@pytest.mark.skipif(_iset3d_available(), reason="iset3d installed")
def test_pbrt_scene_list_missing_dep():
    with pytest.raises(ImportError):
        pbrt_scene_list()
