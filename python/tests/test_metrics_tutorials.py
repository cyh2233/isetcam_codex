from pathlib import Path
import importlib.util
import sys
import matplotlib

matplotlib.use("Agg")


def _load_tutorial(name: str):
    base = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(base))
    path = base / "tutorials" / "metrics" / name
    spec = importlib.util.spec_from_file_location(name[:-3], path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def test_t_metrics_cielab():
    mod = _load_tutorial("t_metrics_cielab.py")
    de76, de94, de2000 = mod.main()
    assert de76 > 0
    assert de94 > 0
    assert de2000 > 0


def test_t_metrics_color():
    mod = _load_tutorial("t_metrics_color.py")
    lstar, delta_e = mod.main()
    assert len(lstar) == 10
    assert len(delta_e) == 10
    assert (delta_e > 0).all()


def test_t_metrics_sqri():
    mod = _load_tutorial("t_metrics_sqri.py")
    sqri, hcsf = mod.main()
    assert sqri > 0
    assert hcsf.size == 1000
