import numpy as np
import pytest
import matplotlib

matplotlib.use("Agg")

from isetcam.opticalimage import OpticalImage, oi_show_image, oi_save_image
from isetcam.display import Display


def _matplotlib_available() -> bool:
    try:
        import matplotlib.pyplot as _  # noqa: F401
        return True
    except Exception:
        return False


@pytest.mark.skipif(not _matplotlib_available(), reason="matplotlib not installed")
def test_oi_show_image_runs():
    wave = np.array([500, 600, 700])
    photons = np.ones((1, 1, 3))
    oi = OpticalImage(photons=photons, wave=wave)
    disp = Display(spd=np.eye(3), wave=wave, gamma=None)
    ax = oi_show_image(oi, disp)
    assert ax is not None


@pytest.mark.skipif(not _matplotlib_available(), reason="matplotlib not installed")
def test_oi_save_image(tmp_path):
    wave = np.array([500, 600, 700])
    photons = np.ones((1, 1, 3))
    oi = OpticalImage(photons=photons, wave=wave)
    disp = Display(spd=np.eye(3), wave=wave, gamma=None)
    path = tmp_path / "oi.png"
    oi_save_image(oi, path, disp)
    import imageio.v2 as imageio

    img = imageio.imread(path)
    assert img.shape == (1, 1, 3)
