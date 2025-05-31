import pytest
import matplotlib

matplotlib.use("Agg")

from isetcam.display import (
    display_create,
    display_list,
    display_plot,
)


def _matplotlib_available() -> bool:
    try:
        import matplotlib.pyplot as _  # noqa: F401
        return True
    except Exception:
        return False


def test_display_list_contains_default():
    names = display_list()
    assert "LCD-Apple" in names


@pytest.mark.skipif(not _matplotlib_available(), reason="matplotlib not installed")
def test_display_plot_variants():
    disp = display_create()
    ax1 = display_plot(disp, kind="spd")
    assert ax1 is not None
    ax2 = display_plot(disp, kind="gamma")
    assert ax2 is not None
    ax3 = display_plot(disp, kind="gamut")
    assert ax3 is not None
