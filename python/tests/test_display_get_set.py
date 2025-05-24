import numpy as np

from isetcam.display import Display, display_get, display_set


def test_display_get_set():
    wave = np.array([500, 510, 520])
    spd = np.ones((3, 2))
    gamma = np.array([[0.0, 0.0], [0.5, 0.5], [1.0, 1.0]])
    disp = Display(spd=spd.copy(), wave=wave, gamma=gamma.copy(), name="orig")

    assert np.allclose(display_get(disp, "spd"), spd)
    assert np.array_equal(display_get(disp, "wave"), wave)
    assert display_get(disp, "n wave") == 3
    assert np.array_equal(display_get(disp, "gamma"), gamma)
    assert display_get(disp, "name") == "orig"

    new_spd = np.zeros_like(spd)
    display_set(disp, "spd", new_spd)
    assert np.allclose(display_get(disp, "spd"), new_spd)

    new_wave = np.array([400, 500])
    display_set(disp, "wave", new_wave)
    assert np.array_equal(display_get(disp, "wave"), new_wave)
    assert display_get(disp, "n_wave") == len(new_wave)

    new_gamma = gamma * 2
    display_set(disp, "gamma", new_gamma)
    assert np.array_equal(display_get(disp, "gamma"), new_gamma)

    display_set(disp, "name", "new")
    assert display_get(disp, "name") == "new"
