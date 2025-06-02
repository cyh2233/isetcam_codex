import numpy as np

from isetcam.io import ie_read_color_filter, ie_save_color_filter


def _sample_data():
    wave = np.array([400, 500, 600], dtype=float)
    spectra = np.array(
        [
            [0.2, 0.1, 0.0],
            [0.5, 0.9, 0.4],
            [0.1, 0.2, 0.8],
        ],
        dtype=float,
    )
    names = ["r", "g", "b"]
    return wave, spectra, names


def test_color_filter_roundtrip_mat(tmp_path):
    wave, spectra, names = _sample_data()
    path = tmp_path / "filters.mat"
    ie_save_color_filter(path, spectra, names, wave)
    loaded, loaded_names, out_wave = ie_read_color_filter(path, wave)
    assert np.array_equal(out_wave, wave)
    assert loaded_names == names
    assert np.allclose(loaded, spectra)


def test_color_filter_roundtrip_text(tmp_path):
    wave, spectra, names = _sample_data()
    path = tmp_path / "filters.txt"
    ie_save_color_filter(path, spectra, names, wave)
    loaded, loaded_names, out_wave = ie_read_color_filter(path, wave)
    assert np.array_equal(out_wave, wave)
    assert loaded_names == names
    assert np.allclose(loaded, spectra)

