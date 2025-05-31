import numpy as np
import pytest
import matplotlib

matplotlib.use("Agg")

from isetcam.scene import Scene, scene_plot


def _mpl_available() -> bool:
    try:
        import matplotlib.pyplot as _  # noqa: F401
        return True
    except Exception:
        return False


@pytest.mark.skipif(not _mpl_available(), reason="matplotlib not installed")
def test_scene_plot_profiles():
    sc = Scene(photons=np.ones((5, 6, 3)), wave=np.array([500, 600, 700]))
    ax1 = scene_plot(sc, kind="luminance hline", loc=2)
    assert ax1 is not None
    ax2 = scene_plot(sc, kind="radiance vline", loc=1)
    assert ax2 is not None


@pytest.mark.skipif(not _mpl_available(), reason="matplotlib not installed")
def test_scene_plot_image_grid_roi():
    sc = Scene(photons=np.ones((4, 4, 3)), wave=np.array([500, 600, 700]))
    ax = scene_plot(sc, kind="radiance image with grid", grid_spacing=2, roi=(1, 1, 2, 2))
    assert ax is not None

