import numpy as np

from isetcam.display import (
    Display,
    display_apply_gamma,
    display_compute,
    display_convert,
    display_from_file,
)
from isetcam.rgb_to_xw_format import rgb_to_xw_format
from isetcam.xw_to_rgb_format import xw_to_rgb_format


def _make_display(n_levels: int = 8) -> Display:
    wave = np.array([500, 510, 520])
    spd = np.eye(3)
    gamma = np.linspace(0, 1, n_levels).reshape(n_levels, 1).repeat(3, axis=1)
    return Display(spd=spd, wave=wave, gamma=gamma)


def test_display_compute_matches_manual():
    disp = _make_display()
    img = np.random.rand(4, 5, 3)

    lin = display_apply_gamma(img, disp)
    xw, r, c = rgb_to_xw_format(lin)
    expected = xw @ disp.spd.T
    expected = xw_to_rgb_format(expected, r, c)

    out = display_compute(img, disp, apply_gamma=True)
    assert np.allclose(out, expected)


def test_display_convert_dict_roundtrip(tmp_path):
    wave = np.array([500, 510])
    spd = np.array([
        [0.1, 0.2],
        [0.3, 0.4],
        [0.5, 0.6],
    ])  # primaries x wave
    gamma = np.linspace(0, 1, 4).reshape(4, 1).repeat(3, axis=1)
    ct_disp = {
        "m_strDisplayName": "demo",
        "sPhysicalDisplay": {
            "m_objCDixelStructure": {
                "m_aWaveLengthSamples": wave,
                "m_aSpectrumOfPrimaries": spd,
                "m_cellGammaStructure": [
                    {"vGammaRampLUT": gamma[:, i]} for i in range(3)
                ],
            },
            "m_fVerticalRefreshRate": 60,
        },
        "sViewingContext": {"m_fViewingDistance": 0.6},
    }

    new_wave = np.array([500, 505, 510])
    out_file = tmp_path / "d.mat"
    disp = display_convert(
        ct_disp,
        wave=new_wave,
        out_file=out_file,
        overwrite=True,
        name="new",
    )

    expected_spd = np.array(
        [np.interp(new_wave, wave, spd[i]) for i in range(spd.shape[0])]
    ).T

    assert isinstance(disp, Display)
    assert disp.name == "new"
    assert np.array_equal(disp.wave, new_wave)
    assert np.allclose(disp.spd, expected_spd)
    assert disp.gamma is not None and np.allclose(disp.gamma, gamma)

    loaded = display_from_file(out_file)
    assert np.allclose(loaded.spd, disp.spd)
    assert np.array_equal(loaded.wave, disp.wave)
    assert loaded.gamma is not None and np.allclose(loaded.gamma, disp.gamma)
