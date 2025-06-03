from pathlib import Path
import importlib.util
import sys
import numpy as np
import matplotlib

matplotlib.use("Agg")


def _load_tutorial(name: str):
    base = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(base))
    path = base / "tutorials" / "optics" / name
    spec = importlib.util.spec_from_file_location(name[:-3], path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def test_t_optics_airy_disk():
    mod = _load_tutorial("t_optics_airy_disk.py")
    shape, total, peak = mod.main()
    assert shape == (64, 64)
    assert np.isclose(total, 1.0)
    assert peak <= 1.0


def test_t_optics_barrel_distortion():
    mod = _load_tutorial("t_optics_barrel_distortion.py")
    rin, rout = mod.main()
    assert np.all(rout < rin)


def test_t_optics_fresnel():
    mod = _load_tutorial("t_optics_fresnel.py")
    e_in, e_out, shape = mod.main()
    assert shape == (32, 32)
    assert np.isclose(e_in, e_out)


def test_t_wvf_mtf():
    mod = _load_tutorial("t_wvf_mtf.py")
    shape, center = mod.main()
    assert shape == (64, 64)
    assert np.isclose(center, 1.0)


def test_t_wvf_zernike():
    mod = _load_tutorial("t_wvf_zernike.py")
    shape, mean_val = mod.main()
    assert shape == (10, 10)
    assert np.isclose(mean_val, 1.0)
