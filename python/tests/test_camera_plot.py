import matplotlib
matplotlib.use("Agg")

import pytest

from isetcam.camera import camera_create, camera_plot


def _mpl_available() -> bool:
    try:
        import matplotlib.pyplot as _  # noqa: F401
        return True
    except Exception:
        return False


@pytest.mark.skipif(not _mpl_available(), reason="matplotlib not installed")
def test_camera_plot_basic():
    cam = camera_create()
    ax_img, ax_mtf = camera_plot(cam)
    assert ax_img is not None
    assert ax_mtf is not None
    assert len(ax_mtf.lines) == 1
