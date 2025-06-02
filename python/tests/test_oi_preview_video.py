import io
import numpy as np
import pytest
import imageio.v2 as imageio

from isetcam.opticalimage import OpticalImage, oi_preview_video


def _ffmpeg_available() -> bool:
    try:
        with imageio.get_writer(io.BytesIO(), format="ffmpeg", fps=1):
            pass
        return True
    except Exception:
        return False


def _gif_available() -> bool:
    try:
        with imageio.get_writer(io.BytesIO(), format="GIF", fps=1):
            pass
        return True
    except Exception:
        return False


@pytest.mark.skipif(not _ffmpeg_available(), reason="ffmpeg not available")
def test_oi_preview_video_mp4(tmp_path):
    wave = np.array([500, 600, 700])
    oi1 = OpticalImage(photons=np.ones((2, 2, 3)) * 1e20, wave=wave)
    oi2 = OpticalImage(photons=np.zeros((2, 2, 3)), wave=wave)
    path = tmp_path / "movie.mp4"
    oi_preview_video([oi1, oi2], path, fps=2)
    reader = imageio.get_reader(path)
    frames = [frame for frame in reader]
    reader.close()
    assert len(frames) == 2
    assert frames[0].shape == (2, 2, 3)


@pytest.mark.skipif(not _gif_available(), reason="GIF support not available")
def test_oi_preview_video_gif(tmp_path):
    wave = np.array([500, 600, 700])
    oi1 = OpticalImage(photons=np.ones((1, 1, 3)) * 1e20, wave=wave)
    oi2 = OpticalImage(photons=np.zeros((1, 1, 3)), wave=wave)
    path = tmp_path / "movie.gif"
    oi_preview_video([oi1, oi2], path, fps=5)
    frames = imageio.mimread(path)
    assert len(frames) == 2
    assert frames[0].shape == (1, 1, 3)
