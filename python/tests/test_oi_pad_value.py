import numpy as np

try:  # pragma: no cover - handle missing requests dependency
    from isetcam.opticalimage import OpticalImage, oi_pad_value
except ModuleNotFoundError:  # pragma: no cover - fallback without requests
    import sys
    import types

    sys.modules.setdefault("requests", types.ModuleType("requests"))
    from isetcam.opticalimage import OpticalImage, oi_pad_value


def _simple_oi(width: int = 3, height: int = 3, n_wave: int = 1) -> OpticalImage:
    wave = np.arange(400, 400 + 10 * n_wave, 10)
    photons = np.arange(width * height * n_wave, dtype=float).reshape(
        (height, width, n_wave)
    )
    oi = OpticalImage(photons=photons, wave=wave)
    oi.sample_spacing = 1e-3  # 1 mm per pixel
    return oi


def test_oi_pad_value_scalar():
    oi = _simple_oi(2, 2, 1)
    out = oi_pad_value(oi, 1, value=-1)

    expected = np.pad(oi.photons, ((1, 1), (1, 1), (0, 0)), constant_values=-1)
    assert np.array_equal(out.photons, expected)

    old_width = oi.photons.shape[1] * oi.sample_spacing
    new_width = out.photons.shape[1] * out.sample_spacing
    assert np.isclose(old_width, new_width)


def test_oi_pad_value_tuple():
    oi = _simple_oi(2, 2, 1)
    out = oi_pad_value(oi, (1, 2, 3, 4), value=5)

    expected = np.pad(
        oi.photons,
        ((1, 2), (3, 4), (0, 0)),
        constant_values=5,
    )
    assert np.array_equal(out.photons, expected)

    old_width = oi.photons.shape[1] * oi.sample_spacing
    new_width = out.photons.shape[1] * out.sample_spacing
    assert np.isclose(old_width, new_width)
