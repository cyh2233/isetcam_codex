import numpy as np

from isetcam.scene import scene_dead_leaves
from isetcam.luminance_from_photons import luminance_from_photons


def test_scene_dead_leaves_shape_and_luminance():
    sc = scene_dead_leaves(patch_size=32, noise_level=0.0, seed=0)
    assert sc.photons.shape == (32, 32, 1)
    lum = luminance_from_photons(sc.photons, sc.wave)
    mean_val = lum.mean()
    # Deterministic mean value for this seed
    assert np.isclose(mean_val, 1.0610504399e-15, rtol=1e-6)
