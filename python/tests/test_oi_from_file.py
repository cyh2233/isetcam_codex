import numpy as np
import scipy.io
from dataclasses import asdict

from isetcam.opticalimage import OpticalImage, oi_from_file


def test_oi_from_file_roundtrip(tmp_path):
    oi = OpticalImage(photons=np.ones((2, 2, 3)), wave=np.array([450, 550, 650]), name="foo")
    path = tmp_path / "oi.mat"
    scipy.io.savemat(path, {"oi": asdict(oi)})

    loaded = oi_from_file(path)
    assert isinstance(loaded, OpticalImage)
    assert np.allclose(loaded.photons, oi.photons)
    assert np.array_equal(loaded.wave, oi.wave)
    assert loaded.name == oi.name


def test_oi_from_file_altvar(tmp_path):
    oi = OpticalImage(photons=np.zeros((1, 1, 1)), wave=np.array([500]), name="bar")
    path = tmp_path / "oi.mat"
    scipy.io.savemat(path, {"opticalimage": asdict(oi)})
    loaded = oi_from_file(path)
    assert np.allclose(loaded.photons, oi.photons)
    assert loaded.name == oi.name

