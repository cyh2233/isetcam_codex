import numpy as np
import pytest

from isetcam.scene import Scene, scene_extract_waveband
from isetcam.opticalimage import OpticalImage, oi_extract_waveband
from isetcam.luminance_from_photons import luminance_from_photons


def _simple_scene(n_wave: int = 4) -> Scene:
    wave = np.arange(400, 400 + 10 * n_wave, 10)
    photons = np.arange(2 * 2 * n_wave, dtype=float).reshape((2, 2, n_wave))
    return Scene(photons=photons, wave=wave)


def _simple_oi(n_wave: int = 4) -> OpticalImage:
    wave = np.arange(500, 500 + 10 * n_wave, 10)
    photons = np.arange(2 * 2 * n_wave, dtype=float).reshape((2, 2, n_wave))
    return OpticalImage(photons=photons, wave=wave)


def test_scene_extract_waveband_basic():
    sc = _simple_scene(4)
    out = scene_extract_waveband(sc, [sc.wave[1], sc.wave[3]])
    assert np.array_equal(out.photons, sc.photons[:, :, [1, 3]])
    assert np.array_equal(out.wave, sc.wave[[1, 3]])


def test_scene_extract_waveband_invalid():
    sc = _simple_scene(3)
    with pytest.raises(ValueError):
        scene_extract_waveband(sc, [999])


def test_oi_extract_waveband_basic():
    oi = _simple_oi(3)
    out = oi_extract_waveband(oi, [oi.wave[0], oi.wave[2]])
    assert np.array_equal(out.photons, oi.photons[:, :, [0, 2]])
    assert np.array_equal(out.wave, oi.wave[[0, 2]])
    assert not hasattr(out, "illuminance")


def test_oi_extract_waveband_illuminance():
    oi = _simple_oi(2)
    out = oi_extract_waveband(oi, [oi.wave[1]], illuminance=True)
    expected = luminance_from_photons(oi.photons[:, :, [1]], oi.wave[[1]])
    assert hasattr(out, "illuminance")
    assert np.allclose(out.illuminance, expected)
