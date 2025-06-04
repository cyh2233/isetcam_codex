import numpy as np
import matplotlib.pyplot as plt

from isetcam import ie_init
from isetcam.illuminant import illuminant_blackbody
from isetcam.ie_xyz_from_energy import ie_xyz_from_energy
from isetcam.srgb_xyz import xyz_to_srgb


def _enlarge(img: np.ndarray, scale: int) -> np.ndarray:
    """Upsample an image by nearest-neighbor replication."""
    return np.kron(img, np.ones((scale, scale, 1)))


def main():
    """Demonstrate simple spectral rendering operations."""
    ie_init()

    wave = np.arange(400, 701, 10)
    spd = illuminant_blackbody(3000, wave)

    fig, ax = plt.subplots()
    ax.plot(wave, spd)
    ax.set_xlabel("Wavelength (nm)")
    ax.set_ylabel("Energy (watts/sr/m^2/nm)")
    ax.grid(True)

    xyz = ie_xyz_from_energy(spd, wave)
    srgb, _, _ = xyz_to_srgb(xyz)

    fig2, ax2 = plt.subplots()
    ax2.imshow(srgb.reshape(1, 1, 3))
    ax2.axis("off")

    spd3 = spd.reshape(1, 1, -1)
    spd_big = _enlarge(spd3, 120)

    spd2 = illuminant_blackbody(8000, wave)
    spd2_big = _enlarge(spd2.reshape(1, 1, -1), 120)

    return srgb.reshape(1, 1, 3).shape, spd_big.shape, spd2_big.shape


if __name__ == "__main__":
    main()
