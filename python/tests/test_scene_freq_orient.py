import numpy as np

from isetcam.scene import scene_freq_orient
from isetcam.scene.imgtargets import img_fo_target
from isetcam.energy_to_quanta import energy_to_quanta

_DEF_WAVE = np.arange(400, 701, 10, dtype=float)


def test_img_fo_target_size():
    params = dict(angles=[0, np.pi/2], freqs=[1, 2], block_size=8, contrast=1)
    img = img_fo_target(
        pattern="sine",
        angles=params["angles"],
        freqs=params["freqs"],
        block_size=params["block_size"],
        contrast=params["contrast"],
    )
    h = len(params["angles"]) * params["block_size"]
    w = len(params["freqs"]) * params["block_size"]
    assert img.shape == (h, w)
    assert img.max() <= 1.0 and img.min() >= 1e-6


def test_scene_freq_orient_blocks():
    angles = [0, np.pi / 2]
    freqs = [1]
    block_size = 8
    sc = scene_freq_orient(
        {
            "angles": angles,
            "freqs": freqs,
            "block_size": block_size,
            "contrast": 1,
        }
    )
    assert sc.photons.shape == (
        len(angles) * block_size,
        len(freqs) * block_size,
        _DEF_WAVE.size,
    )
    ill = energy_to_quanta(_DEF_WAVE, np.ones_like(_DEF_WAVE)).ravel()
    assert np.allclose(sc.illuminant, ill)

    x = np.arange(block_size) / block_size
    X, Y = np.meshgrid(x, x)
    top = 0.5 * (1 + np.sin(2 * np.pi * freqs[0] * Y))
    bottom = 0.5 * (1 + np.sin(2 * np.pi * freqs[0] * X))
    top = np.clip(top, 1e-6, 1.0) / top.max()
    bottom = np.clip(bottom, 1e-6, 1.0) / bottom.max()
    expected_top = top * ill[0]
    expected_bottom = bottom * ill[0]
    assert np.allclose(sc.photons[:block_size, :block_size, 0], expected_top)
    assert np.allclose(sc.photons[block_size:, :block_size, 0], expected_bottom)
