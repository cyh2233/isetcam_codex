import numpy as np
import scipy.io
from dataclasses import asdict

from isetcam.display import Display, display_from_file


def test_display_from_file_roundtrip(tmp_path):
    disp = Display(
        spd=np.ones((2, 3)),
        wave=np.array([500, 510]),
        gamma=np.linspace(0, 1, 4).reshape(4, 1).repeat(3, axis=1),
        name="demo",
    )
    path = tmp_path / "d.mat"
    scipy.io.savemat(path, {"d": asdict(disp)})

    loaded = display_from_file(path)
    assert isinstance(loaded, Display)
    assert np.allclose(loaded.spd, disp.spd)
    assert np.array_equal(loaded.wave, disp.wave)
    assert loaded.gamma is not None and np.allclose(loaded.gamma, disp.gamma)
