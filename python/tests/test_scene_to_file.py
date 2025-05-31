import numpy as np
import scipy.io

from isetcam.scene import scene_from_file, scene_to_file
from isetcam import data_path


def test_scene_to_file_roundtrip(tmp_path):
    fpath = data_path('images/rgb/adelson.png')
    wave = np.array([450, 550, 650, 750])
    scene = scene_from_file(fpath, wave=wave)

    mat_path = tmp_path / 'scene.mat'
    scene_to_file(scene, mat_path)

    mat = scipy.io.loadmat(mat_path, squeeze_me=True, struct_as_record=False)
    assert 'scene' in mat
    saved = mat['scene']
    assert np.allclose(saved.photons, scene.photons)
    assert np.array_equal(saved.wave.reshape(-1), scene.wave)

