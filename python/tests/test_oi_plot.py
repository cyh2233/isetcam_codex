import numpy as np
import pytest
import matplotlib

matplotlib.use("Agg")

from isetcam.opticalimage import OpticalImage, oi_plot


def _mpl_available() -> bool:
    try:
        import matplotlib.pyplot as _  # noqa: F401
        return True
    except Exception:
        return False


@pytest.mark.skipif(not _mpl_available(), reason="matplotlib not installed")
def test_oi_plot_profiles():
    oi = OpticalImage(photons=np.ones((5, 6, 3)), wave=np.array([500, 600, 700]))
    ax1 = oi_plot(oi, kind="illuminance hline", loc=2)
    assert ax1 is not None
    ax2 = oi_plot(oi, kind="irradiance vline", loc=1)
    assert ax2 is not None


@pytest.mark.skipif(not _mpl_available(), reason="matplotlib not installed")
def test_oi_plot_image_grid_roi():
    oi = OpticalImage(photons=np.ones((4, 4, 3)), wave=np.array([500, 600, 700]))
    ax = oi_plot(oi, kind="irradiance image with grid", grid_spacing=2, roi=(1, 1, 2, 2))
    assert ax is not None

