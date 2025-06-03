from pathlib import Path
import importlib.util
import sys
import matplotlib

matplotlib.use("Agg")


def _load_tutorial(name: str):
    base = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(base))
    path = base / "tutorials" / "oi" / name
    spec = importlib.util.spec_from_file_location(name[:-3], path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def test_t_oi_introduction():
    mod = _load_tutorial("t_oi_introduction.py")
    fn_small, fn_big = mod.main()
    assert fn_big > fn_small > 0


def test_t_oi_principles():
    mod = _load_tutorial("t_oi_principles.py")
    p1, p2 = mod.main()
    assert p1 > 0 and p2 > p1


def test_t_oi_radiance_to_irradiance():
    mod = _load_tutorial("t_oi_radiance_to_irradiance.py")
    irr = mod.main()
    assert irr.size == 5


def test_t_oi_rt_compute():
    mod = _load_tutorial("t_oi_rt_compute.py")
    model = mod.main()
    assert model == "ray trace"
