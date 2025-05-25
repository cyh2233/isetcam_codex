import numpy as np

from isetcam.display import Display, display_from_file, display_to_file


def test_display_to_file_roundtrip(tmp_path):
    disp = Display(
        spd=np.ones((2, 3)),
        wave=np.array([500, 510]),
        gamma=np.linspace(0, 1, 4).reshape(4, 1).repeat(3, axis=1),
        name="demo",
    )
    path = tmp_path / "d.mat"
    display_to_file(disp, path)

    loaded = display_from_file(path)
    assert isinstance(loaded, Display)
    assert np.allclose(loaded.spd, disp.spd)
    assert np.array_equal(loaded.wave, disp.wave)
    assert loaded.gamma is not None and np.allclose(loaded.gamma, disp.gamma)
