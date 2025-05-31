import numpy as np

from isetcam.ip import VCImage, ip_to_file, ip_from_file


def test_ip_file_roundtrip(tmp_path):
    ip = VCImage(rgb=np.ones((2, 2, 3)), wave=np.array([500, 510, 520]), name="demo")
    path = tmp_path / "ip.mat"
    ip_to_file(ip, path)

    loaded = ip_from_file(path)
    assert isinstance(loaded, VCImage)
    assert np.allclose(loaded.rgb, ip.rgb)
    assert np.array_equal(loaded.wave, ip.wave)
    assert loaded.name == ip.name
