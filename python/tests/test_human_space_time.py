import numpy as np
from isetcam.human import (
    human_space_time,
    kelly_space_time,
    westheimer_lsf,
    poirson_spatio_chromatic,
)


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


def _gauss2(hwhm_y: float, support_y: int, hwhm_x: float, support_x: int) -> np.ndarray:
    x = np.arange(support_x) - round(support_x / 2)
    y = np.arange(support_y) - round(support_y / 2)
    X, Y = np.meshgrid(x, y)
    sd_x = hwhm_x / np.sqrt(2 * np.log(2))
    sd_y = hwhm_y / np.sqrt(2 * np.log(2))
    g = np.exp(-0.5 * ((X / sd_x) ** 2 + (Y / sd_y) ** 2))
    return g / g.sum()


def _sum_gauss(params: list[float]) -> np.ndarray:
    width = int(round(params[0]))
    g = np.zeros((width, width), dtype=float)
    n = (len(params) - 1) // 2
    for i in range(n):
        h = params[2 * i + 1]
        w = params[2 * i + 2]
        g += w * _gauss2(h, width, h, width)
    return g / g.sum()


def _poirson_expected():
    samp = 241.0
    x1 = np.array([0.05, 0.9207, 0.225, 0.105, 7.0, -0.1080])
    x2 = np.array([0.0685, 0.5310, 0.826, 0.33])
    x3 = np.array([0.0920, 0.4877, 0.6451, 0.3711])
    x1[[0, 2, 4]] *= samp
    x2[[0, 2]] *= samp
    x3[[0, 2]] *= samp
    width = int(np.ceil(samp / 2) * 2 - 1)
    lum = _sum_gauss([width, *x1])
    rg = _sum_gauss([width, *x2])
    by = _sum_gauss([width, *x3])
    pos = (np.arange(width) - (width + 1) / 2) / samp
    return lum, rg, by, pos


def test_poirson_spatio_chromatic_defaults():
    lum, rg, by, pos = poirson_spatio_chromatic()
    exp_lum, exp_rg, exp_by, exp_pos = _poirson_expected()
    assert np.allclose(lum, exp_lum)
    assert np.allclose(rg, exp_rg)
    assert np.allclose(by, exp_by)
    assert np.allclose(pos, exp_pos)


def test_human_space_time_poirson():
    sens, fs, ft = human_space_time("poirsoncolor")
    exp_lum, exp_rg, exp_by, exp_pos = _poirson_expected()
    assert np.array_equal(fs, exp_pos)
    assert np.array_equal(ft, 10 ** np.arange(-0.5, 1.7 + 0.05, 0.05))
    assert np.allclose(sens["lum"], exp_lum)
    assert np.allclose(sens["rg"], exp_rg)
    assert np.allclose(sens["by"], exp_by)
