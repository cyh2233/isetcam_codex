from pathlib import Path
import importlib.util
import sys
import matplotlib

matplotlib.use("Agg")


def _load_tutorial(name: str):
    base = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(base))
    path = base / "tutorials" / "image" / name
    spec = importlib.util.spec_from_file_location(name[:-3], path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def test_t_ip():
    mod = _load_tutorial("t_ip.py")
    shape = mod.main()
    assert len(shape) == 3 and shape[2] == 3


def test_t_ip_demosaic():
    mod = _load_tutorial("t_ip_demosaic.py")
    s1, s2 = mod.main()
    assert s1 == s2
    assert s1[2] == 3


def test_t_ip_jpeg_monochrome():
    mod = _load_tutorial("t_ip_jpeg_monochrome.py")
    im_shape, coef_shape, rec_shape = mod.main()
    assert coef_shape == im_shape
    assert rec_shape == im_shape


def test_t_ip_jpeg_color():
    mod = _load_tutorial("t_ip_jpeg_color.py")
    orig_shape, jpeg_shape = mod.main()
    assert orig_shape == jpeg_shape
    assert orig_shape[2] == 3
