import numpy as np
import matplotlib

matplotlib.use("Agg")

from isetcam import chromaticity_plot


def test_chromaticity_plot_runs():
    x = np.array([0.3, 0.4])
    y = np.array([0.3, 0.4])
    ax = chromaticity_plot(x, y)
    assert ax is not None


def test_chromaticity_plot_reuse_axis():
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots()
    x = np.array([0.2])
    y = np.array([0.3])
    ax2 = chromaticity_plot(x, y, ax=ax)
    assert ax2 is ax
