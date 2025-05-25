import numpy as np

from isetcam.opticalimage import OpticalImage, oi_from_file, oi_to_file


def test_oi_to_file_roundtrip(tmp_path):
    oi = OpticalImage(photons=np.ones((2, 2, 3)), wave=np.array([450, 550, 650]), name="foo")
    path = tmp_path / "oi.mat"
    oi_to_file(oi, path)

    loaded = oi_from_file(path)
    assert isinstance(loaded, OpticalImage)
    assert np.allclose(loaded.photons, oi.photons)
    assert np.array_equal(loaded.wave, oi.wave)
    assert loaded.name == oi.name
