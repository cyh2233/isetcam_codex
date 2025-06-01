import io
import numpy as np
import pytest
import imageio.v2 as imageio

from isetcam.scene import Scene, scene_make_video


def _ffmpeg_available() -> bool:
    try:
        with imageio.get_writer(io.BytesIO(), format="ffmpeg", fps=1):
            pass
        return True
    except Exception:
        return False


@pytest.mark.skipif(not _ffmpeg_available(), reason="ffmpeg not available")
def test_scene_make_video(tmp_path):
    wave = np.array([500, 600, 700])
    sc1 = Scene(photons=np.ones((2, 2, 3)), wave=wave)
    sc2 = Scene(photons=np.zeros((2, 2, 3)), wave=wave)
    path = tmp_path / "movie.mp4"
    scene_make_video([sc1, sc2], path, fps=2)
    reader = imageio.get_reader(path)
    frames = [frame for frame in reader]
    reader.close()
    assert len(frames) == 2
    assert frames[0].shape == (2, 2, 3)
