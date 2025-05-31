import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt

from isetcam import ie_format_figure, set_ie_figure_defaults, _IE_FIGURE_DEFAULTS


def test_ie_format_figure_basic():
    fig, ax = plt.subplots()
    ax.plot([0, 1], [0, 1])
    ie_format_figure(ax, xlabel="x", ylabel="y", font_size=11, grid=True)
    assert ax.get_xlabel() == "x"
    assert ax.get_ylabel() == "y"
    assert ax.xaxis.label.get_size() == 11
    assert all(gl.get_visible() for gl in ax.xaxis.get_gridlines())


def test_set_ie_figure_defaults():
    old_size = _IE_FIGURE_DEFAULTS["font_size"]
    set_ie_figure_defaults(font_size=8)
    fig, ax = plt.subplots()
    ax.plot([0, 1], [0, 1])
    ie_format_figure(ax, xlabel="a", ylabel="b")
    assert ax.xaxis.label.get_size() == 8
    set_ie_figure_defaults(font_size=old_size)
