from pathlib import Path
import importlib.util
import sys
import matplotlib

matplotlib.use("Agg")


def _load_tutorial(name: str):
    base = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(base))
    path = base / "tutorials" / "color" / name
    spec = importlib.util.spec_from_file_location(name[:-3], path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def test_t_color_energy_quanta():
    mod = _load_tutorial("t_color_energy_quanta.py")
    energy, d65_energy, d65_photons, xyz_e, xyz_q = mod.main()
    assert energy.shape[0] == 61
    assert d65_energy.shape[0] == 61
    assert d65_photons.shape[0] == 61
    assert xyz_e.shape == (61, 3)
    assert xyz_q.shape == (61, 3)


def test_t_color_chromaticity():
    mod = _load_tutorial("t_color_chromaticity.py")
    xy_white, xy_primaries, xy_scene = mod.main()
    assert xy_white.shape[-1] == 2
    assert xy_primaries.shape == (3, 2)
    assert xy_scene.shape[1] == 2


def test_t_color_spectrum():
    mod = _load_tutorial("t_color_spectrum.py")
    rgb_spectrum, srgb = mod.main()
    assert rgb_spectrum.shape[1] == 3
    assert srgb.shape == rgb_spectrum.shape


def test_t_color_matching():
    mod = _load_tutorial("t_color_matching.py")
    rgb2xyz, xyz2rgb, srgb = mod.main()
    assert rgb2xyz.shape == (3, 3)
    assert xyz2rgb.shape == (3, 3)
    assert srgb.shape == (3,)
