from pathlib import Path
import importlib.util
import sys
import matplotlib

matplotlib.use("Agg")


def _load_tutorial(name: str):
    base = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(base))
    path = base / "tutorials" / "code" / name
    spec = importlib.util.spec_from_file_location(name[:-3], path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def test_t_code_objects():
    mod = _load_tutorial("t_code_objects.py")
    idx, shape = mod.main()
    assert idx >= 1
    assert len(shape) == 3


def test_t_code_rendering():
    mod = _load_tutorial("t_code_rendering.py")
    srgb_shape, spd1_shape, spd2_shape = mod.main()
    assert srgb_shape == (1, 1, 3)
    assert spd1_shape[0] == spd1_shape[1] == 120
    assert spd2_shape[0] == spd2_shape[1] == 120


def test_t_code_session():
    mod = _load_tutorial("t_code_session.py")
    counts, shape = mod.main()
    before, after, final = counts
    assert after == before + 2
    assert final == after + 1
    assert len(shape) == 3


def test_t_code_startup():
    mod = _load_tutorial("t_code_startup.py")
    before, after, root = mod.main()
    assert after
    assert root in sys.path
