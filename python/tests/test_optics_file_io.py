import numpy as np

from isetcam.optics import Optics, optics_from_file, optics_to_file


def test_optics_file_roundtrip(tmp_path):
    opt = Optics(
        f_number=4.0,
        f_length=0.004,
        wave=np.array([500, 510]),
        transmittance=np.array([1.0, 0.9]),
        name="demo",
    )
    path = tmp_path / "optics.mat"
    optics_to_file(opt, path)

    loaded = optics_from_file(path)
    assert isinstance(loaded, Optics)
    assert loaded.f_number == opt.f_number
    assert loaded.f_length == opt.f_length
    assert np.array_equal(loaded.wave, opt.wave)
    assert np.allclose(loaded.transmittance, opt.transmittance)
    assert loaded.name == opt.name
