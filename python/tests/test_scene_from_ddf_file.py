import json
import io
from zipfile import ZipFile

import numpy as np

from isetcam.scene import scene_from_ddf_file, Scene


def _write_sample_ddf(path):
    photons = np.arange(12, dtype=float).reshape(2, 2, 3)
    wave = np.array([450.0, 550.0, 650.0], dtype=float)
    meta = {"width": 2, "height": 2, "nwave": 3}

    with ZipFile(path, "w") as z:
        z.writestr("metadata.json", json.dumps(meta))
        buf = io.BytesIO(); np.save(buf, photons); z.writestr("photons.npy", buf.getvalue())
        buf = io.BytesIO(); np.save(buf, wave); z.writestr("wave.npy", buf.getvalue())

    return photons, wave


def test_scene_from_ddf_file(tmp_path):
    ddf_path = tmp_path / "sample.ddf"
    photons, wave = _write_sample_ddf(ddf_path)

    sc = scene_from_ddf_file(ddf_path)
    assert isinstance(sc, Scene)
    assert np.allclose(sc.photons, photons)
    assert np.array_equal(sc.wave, wave)

