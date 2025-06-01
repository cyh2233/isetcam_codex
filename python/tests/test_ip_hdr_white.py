import numpy as np

from isetcam.ip import VCImage, ip_hdr_white


def _simple_ip() -> VCImage:
    rgb = np.array(
        [
            [[0.5, 0.5, 0.5], [0.9, 0.9, 0.9]],
            [[1.0, 1.0, 1.0], [0.2, 0.2, 0.2]],
        ],
        dtype=float,
    )
    wave = np.array([500, 510, 520])
    return VCImage(rgb=rgb, wave=wave)


def test_ip_hdr_white_default():
    ip = _simple_ip()
    out, w = ip_hdr_white(ip, saturation=1.0, hdr_level=0.8, wgt_blur=0)
    assert out is ip
    lum = out.rgb.mean(axis=2)
    assert np.isclose(lum.max(), 1.0)
    assert w.shape == lum.shape
    assert np.isclose(w[1, 0], 1.0)


def test_ip_hdr_white_scaled():
    ip = _simple_ip()
    out, _ = ip_hdr_white(ip, saturation=1.0, hdr_level=0.8, wgt_blur=0, white_level=0.5)
    lum = out.rgb.mean(axis=2)
    assert np.isclose(lum.max(), 0.5)
