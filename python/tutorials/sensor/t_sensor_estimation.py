import numpy as np
import matplotlib.pyplot as plt
from isetcam import ie_init, ie_read_spectra, data_path


def _load_spectra(name: str, wave: np.ndarray) -> np.ndarray:
    """Try loading a spectra by name with fall backs to data files."""
    try:
        spectra, _, _, _ = ie_read_spectra(name, wave)
        return spectra
    except Exception:
        pass

    candidates = [
        name,
        name + ".mat" if not name.endswith(".mat") else name,
        f"surfaces/reflectances/{name}",
        f"lights/{name}",
        f"scripts/color/{name}",
        f"surfaces/reflectances/{name}.mat",
        f"lights/{name}.mat",
        f"scripts/color/{name}.mat",
    ]

    for cand in candidates:
        path = data_path(cand)
        if path.exists():
            spectra, _, _, _ = ie_read_spectra(path, wave)
            return spectra

    raise FileNotFoundError(name)


def main():
    """Estimate sensor quantum efficiency from Macbeth chart data."""
    ie_init()

    wave = np.arange(400, 701, 10)
    refl = _load_spectra("macbethChart", wave)
    d65 = _load_spectra("lights/D65.mat", wave)

    try:
        qe = _load_spectra("cMatch/camera", wave)
    except Exception:
        # Simple Gaussian example QE curves
        centers = np.array([460, 550, 610])
        qe = np.exp(-0.5 * ((wave[:, None] - centers) / 20) ** 2)

    # Scattered light reaching the sensor
    spd = d65 * refl

    # True sensor responses
    rgb = qe.T @ spd

    # Estimate QE from responses
    qe_est = (rgb @ np.linalg.pinv(spd)).T

    # Predicted responses using estimated QE
    rgb_est = qe_est.T @ spd

    fig, (ax1, ax2) = plt.subplots(2, 1)
    ax1.plot(wave, qe)
    ax1.plot(wave, qe_est, "--")
    ax1.set_xlabel("Wavelength (nm)")
    ax1.set_ylabel("Quantum efficiency")

    ax2.plot(rgb.T)
    ax2.plot(rgb_est.T, "--")
    ax2.set_xlabel("Patch")
    ax2.set_ylabel("RGB response")
    plt.tight_layout()

    return qe_est.shape, rgb_est.shape


if __name__ == "__main__":
    main()
