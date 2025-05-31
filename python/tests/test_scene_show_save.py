import numpy as np
import pytest
import matplotlib

matplotlib.use("Agg")

from isetcam.scene import Scene, scene_show_image, scene_save_image


def _matplotlib_available() -> bool:
    try:
        import matplotlib.pyplot as _  # noqa: F401
        return True
    except Exception:
        return False


@pytest.mark.skipif(not _matplotlib_available(), reason="matplotlib not installed")
def test_scene_show_image_runs():
    sc = Scene(photons=np.ones((1, 1, 3)), wave=np.array([500, 600, 700]))
    ax = scene_show_image(sc)
    assert ax is not None


@pytest.mark.skipif(not _matplotlib_available(), reason="matplotlib not installed")
def test_scene_save_image(tmp_path):
    sc = Scene(photons=np.ones((1, 1, 3)), wave=np.array([500, 600, 700]))
    path = tmp_path / "out.png"
    scene_save_image(sc, path)
    import imageio.v2 as imageio

    img = imageio.imread(path)
    assert img.shape == (1, 1, 3)
