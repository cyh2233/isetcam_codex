import io
import numpy as np
import pytest
import imageio.v2 as imageio

from isetcam import animated_gif


def _gif_available() -> bool:
    try:
        with imageio.get_writer(io.BytesIO(), format="GIF", fps=1):
            pass
        return True
    except Exception:
        return False


@pytest.mark.skipif(not _gif_available(), reason="GIF support not available")
def test_animated_gif_list(tmp_path):
    frames = [
        np.zeros((2, 2, 3), dtype=float),
        np.ones((2, 2, 3), dtype=float),
    ]
    path = tmp_path / "out.gif"
    animated_gif(frames, path, fps=2, loop=0)
    loaded = imageio.mimread(path)
    assert len(loaded) == 2
    assert loaded[0].shape == (2, 2, 3)
    assert loaded[0].dtype == np.uint8
    assert loaded[0].min() == 0 and loaded[1].max() == 255


@pytest.mark.skipif(not _gif_available(), reason="GIF support not available")
def test_animated_gif_array(tmp_path):
    arr = np.stack([
        np.zeros((1, 1, 3), dtype=float),
        np.ones((1, 1, 3), dtype=float),
    ], axis=0)
    path = tmp_path / "out_arr.gif"
    animated_gif(arr, path, fps=5, loop=1)
    loaded = imageio.mimread(path)
    assert len(loaded) == 2
    assert loaded[0].shape == (1, 1, 3)

