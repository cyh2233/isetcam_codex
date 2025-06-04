from pathlib import Path
import importlib.util
import sys
import matplotlib

matplotlib.use("Agg")


def _load_tutorial():
    base = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(base))
    path = base / "tutorials" / "introduction" / "t_introduction_to_iset.py"
    spec = importlib.util.spec_from_file_location("t_introduction_to_iset", path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def test_t_introduction_to_iset_exec():
    mod = _load_tutorial()
    shapes = mod.main()
    assert len(shapes) == 4
    scene_shape, oi_shape, sensor_shape, rgb_shape = shapes
    assert rgb_shape[-1] == 3
    assert sensor_shape[0] == rgb_shape[0]
    assert scene_shape[0] == oi_shape[0]
