import numpy as np
import pytest
import matplotlib

matplotlib.use("Agg")

from isetcam.sensor import Sensor, sensor_plot


def _matplotlib_available() -> bool:
    try:
        import matplotlib.pyplot as _  # noqa: F401
        return True
    except Exception:
        return False


@pytest.mark.skipif(not _matplotlib_available(), reason="matplotlib not installed")
def test_sensor_plot_runs():
    s = Sensor(volts=np.array([[0.1, 0.2], [0.3, 0.4]]), wave=np.array([500]), exposure_time=0.01)
    s.filter_color_letters = "rggb"
    ax = sensor_plot(s, show_filters=True)
    assert ax is not None


@pytest.mark.skipif(not _matplotlib_available(), reason="matplotlib not installed")
def test_sensor_plot_reuse_axis():
    import matplotlib.pyplot as plt

    s = Sensor(volts=np.zeros((2, 2)), wave=np.array([500]), exposure_time=0.01)
    fig, ax = plt.subplots()
    ax2 = sensor_plot(s, ax=ax)
    assert ax2 is ax
