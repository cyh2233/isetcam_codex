import numpy as np
import pytest
import matplotlib

matplotlib.use("Agg")

from isetcam.ip import VCImage, ip_plot


def _mpl_available() -> bool:
    try:
        import matplotlib.pyplot as _  # noqa: F401
        return True
    except Exception:
        return False


@pytest.mark.skipif(not _mpl_available(), reason="matplotlib not installed")
def test_ip_plot_profiles():
    ip = VCImage(rgb=np.ones((5, 6, 3)), wave=np.array([500, 600, 700]))
    ax1 = ip_plot(ip, kind="horizontal line luminance", loc=2)
    assert ax1 is not None
    ax2 = ip_plot(ip, kind="vertical line luminance", loc=1)
    assert ax2 is not None


@pytest.mark.skipif(not _mpl_available(), reason="matplotlib not installed")
def test_ip_plot_image_grid_roi():
    ip = VCImage(rgb=np.ones((4, 4, 3)), wave=np.array([500, 600, 700]))
    ax = ip_plot(ip, kind="image with grid", grid_spacing=2, roi=(1, 1, 2, 2))
    assert ax is not None

