import numpy as np
import pytest

from isetcam.camera import camera_create, camera_mtf


def _expected(freqs, camera):
    pixel = getattr(camera.sensor, "pixel_size", 2.8e-6)
    f_number = getattr(camera.optics, "f_number", 4.0)
    wave = np.mean(camera.sensor.wave) * 1e-9
    f_cutoff = 1.0 / (wave * f_number) / 1e3
    pixel_mtf = np.abs(np.sinc(freqs * pixel * 1e3))
    nf = freqs / f_cutoff
    optics_mtf = np.zeros_like(freqs)
    inside = nf <= 1.0
    f = nf[inside]
    optics_mtf[inside] = (2 / np.pi) * (np.arccos(f) - f * np.sqrt(1 - f ** 2))
    return pixel_mtf * optics_mtf


def test_camera_mtf_default():
    cam = camera_create()
    freqs, mtf = camera_mtf(cam)
    expected = _expected(freqs, cam)
    assert np.allclose(mtf, expected)
    assert freqs[0] == pytest.approx(0.0)
    assert mtf[0] == pytest.approx(1.0)
    assert mtf[-1] <= 1.0


def test_camera_mtf_custom_freq_and_error():
    cam = camera_create()
    f = np.linspace(0, 50, 10)
    freqs, mtf = camera_mtf(cam, f)
    expected = _expected(f, cam)
    assert np.allclose(freqs, f)
    assert np.allclose(mtf, expected)
    with pytest.raises(ValueError):
        camera_mtf(cam, f, method="unknown")
