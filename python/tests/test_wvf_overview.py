from pathlib import Path
import importlib.util
import sys
import matplotlib

matplotlib.use("Agg")


def _load_tutorial():
    base = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(base))
    path = base / "tutorials" / "optics" / "t_wvf_overview.py"
    spec = importlib.util.spec_from_file_location("t_wvf_overview", path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def test_wvf_overview_shapes():
    mod = _load_tutorial()
    wvf_shape, psf_shape, mtf_shape = mod.main()
    assert wvf_shape == psf_shape == mtf_shape
    assert wvf_shape == (64, 64)
