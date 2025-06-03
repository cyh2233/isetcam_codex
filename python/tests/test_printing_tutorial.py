from pathlib import Path
import importlib.util
import sys
import numpy as np
import matplotlib

matplotlib.use("Agg")


def _load_tutorial():
    base = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(base))
    path = base / "tutorials" / "printing" / "t_printing_halftone.py"
    spec = importlib.util.spec_from_file_location("t_printing_halftone", path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def test_t_printing_halftone():
    mod = _load_tutorial()
    ht_dither, ht_error = mod.main()
    assert ht_dither.shape == (64, 64)
    assert ht_error.shape == (64, 64)
    assert set(np.unique(ht_dither)).issubset({0, 1})
    assert set(np.unique(ht_error)).issubset({0, 1})
