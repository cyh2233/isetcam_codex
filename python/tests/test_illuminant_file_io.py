import numpy as np

from isetcam.illuminant import Illuminant, illuminant_from_file, illuminant_to_file


def test_illuminant_file_roundtrip(tmp_path):
    illum = Illuminant(spd=np.array([1.0, 0.5]), wave=np.array([500, 600]), name="demo")
    path = tmp_path / "illum.mat"
    illuminant_to_file(illum, path)

    loaded = illuminant_from_file(path)
    assert isinstance(loaded, Illuminant)
    assert np.allclose(loaded.spd, illum.spd)
    assert np.array_equal(loaded.wave, illum.wave)
    assert loaded.name == illum.name
