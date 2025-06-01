import numpy as np
from isetcam.human import human_space_time, kelly_space_time, westheimer_lsf


def _kelly_expected():
    fs = 10 ** np.arange(-0.5, 1.3 + 0.05, 0.05)
    ft = 10 ** np.arange(-0.5, 1.7 + 0.05, 0.05)
    ft_grid, fs_grid = np.meshgrid(ft, fs)
    alpha = 2 * np.pi * fs_grid
    v = ft_grid / fs_grid
    k = 6.1 + 7.3 * (np.abs(np.log10(v / 3))) ** 3
    amax = 45.9 / (v + 2)
    sens = k * v * (alpha ** 2) * np.exp(-2 * alpha / amax)
    sens[sens < 1] = np.nan
    sens = sens / 2
    return sens, fs, ft


def test_kelly_space_time_defaults():
    sens, fs, ft = kelly_space_time()
    exp_sens, exp_fs, exp_ft = _kelly_expected()
    assert np.array_equal(fs, exp_fs)
    assert np.array_equal(ft, exp_ft)
    assert np.allclose(sens, exp_sens, equal_nan=True)


def test_human_space_time_defaults():
    sens, fs, ft = human_space_time()
    exp_sens, exp_fs, exp_ft = _kelly_expected()
    assert np.array_equal(fs, exp_fs)
    assert np.array_equal(ft, exp_ft)
    assert np.allclose(sens, exp_sens, equal_nan=True)


def test_westheimer_lsf_defaults():
    ls, x = westheimer_lsf()
    x_min = x / 60.0
    exp = 0.47 * np.exp(-3.3 * (x_min ** 2)) + 0.53 * np.exp(-0.93 * np.abs(x_min))
    exp = exp / exp.sum()
    assert np.allclose(ls, exp)
