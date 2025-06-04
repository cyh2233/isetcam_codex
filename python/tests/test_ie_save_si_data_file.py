import numpy as np
import scipy.io

from isetcam.io import ie_save_si_data_file


def test_ie_save_si_data_file_roundtrip(tmp_path):
    psf = np.random.rand(4, 4, 2)
    wave = np.array([500, 600])
    up = [0.1, 0.1]
    path = tmp_path / "psf.mat"
    ie_save_si_data_file(path, psf, wave, up)

    data = scipy.io.loadmat(path, squeeze_me=True, struct_as_record=False)
    assert np.allclose(data["psf"], psf)
    assert np.allclose(data["wave"], wave)
    assert np.allclose(data["umPerSamp"], up)
    notes = data["notes"]
    if hasattr(notes, "__dict__"):
        assert "timeStamp" in notes.__dict__
    else:
        assert "timeStamp" in notes
