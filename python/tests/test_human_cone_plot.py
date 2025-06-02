import matplotlib
matplotlib.use("Agg")

from isetcam.human import human_cone_mosaic, human_cone_plot


def test_human_cone_plot_runs():
    xy, cone_type, _, _ = human_cone_mosaic((5, 5), r_seed=1)
    ax = human_cone_plot(xy, cone_type)
    assert ax is not None
