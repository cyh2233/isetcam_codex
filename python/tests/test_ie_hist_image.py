import numpy as np
import pytest
import matplotlib

matplotlib.use("Agg")

from isetcam import ie_hist_image


def _matplotlib_available() -> bool:
    try:
        import matplotlib.pyplot as _  # noqa: F401
        return True
    except Exception:
        return False


@pytest.mark.skipif(not _matplotlib_available(), reason="matplotlib not installed")
def test_ie_hist_image_gray():
    img = np.random.rand(10, 10)
    ax = ie_hist_image(img)
    assert ax is not None


@pytest.mark.skipif(not _matplotlib_available(), reason="matplotlib not installed")
def test_ie_hist_image_rgb_reuse_axis():
    import matplotlib.pyplot as plt

    img = np.random.rand(5, 5, 3)
    fig, ax = plt.subplots()
    ax2 = ie_hist_image(img, ax=ax)
    assert ax2 is ax
