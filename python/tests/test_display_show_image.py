import numpy as np
import pytest
import matplotlib

matplotlib.use("Agg")

from isetcam.display import Display, display_show_image


def _matplotlib_available() -> bool:
    try:
        import matplotlib.pyplot as _  # noqa: F401
        return True
    except Exception:
        return False


@pytest.mark.skipif(not _matplotlib_available(), reason="matplotlib not installed")
def test_display_show_image_runs():
    img = np.array([[[0.2, 0.4, 0.6]]], dtype=float)
    disp = Display(spd=np.ones((1, 3)), wave=np.array([500]), gamma=None)
    ax = display_show_image(img, disp)
    assert ax is not None
