import numpy as np

from isetcam.ip import VCImage, ip_clear_data


def _simple_ip() -> VCImage:
    rgb = np.ones((2, 2, 3), dtype=float)
    wave = np.array([500, 510, 520])
    return VCImage(rgb=rgb, wave=wave)


def test_ip_clear_data_removes_fields():
    ip = _simple_ip()
    ip.processed_rgb = np.zeros_like(ip.rgb)
    ip.custom_attr = 42

    out = ip_clear_data(ip)
    assert out is ip
    for fld in ["processed_rgb", "custom_attr"]:
        assert not hasattr(out, fld)


def test_ip_clear_data_no_fields():
    ip = _simple_ip()
    out = ip_clear_data(ip)
    assert out is ip
    assert np.allclose(out.rgb, ip.rgb)
    assert np.array_equal(out.wave, ip.wave)
