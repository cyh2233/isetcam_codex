import numpy as np
from isetcam import ie_init, data_path, ie_read_spectra
from isetcam.metrics import delta_e_ab
from isetcam.xyz_to_lab import xyz_to_lab


def main():
    """Explore CIELAB values for a set of gray surfaces."""
    ie_init()

    wave = np.arange(400, 701, 10)
    gray_surfaces = np.outer(np.ones_like(wave, dtype=float), np.linspace(0.1, 1.0, 10))

    d65, _, _, _ = ie_read_spectra(data_path("lights/D65.mat"), wave)
    xyz_cmfs, _, _, _ = ie_read_spectra(data_path("human/XYZ.mat"), wave)

    gray_spd = d65[:, 0][:, None] * gray_surfaces
    gray_xyz = xyz_cmfs.T @ gray_spd
    gray_xyz = gray_xyz * 100.0 / gray_xyz[1, -1]
    white_xyz = gray_xyz[:, -1]

    lab1 = xyz_to_lab(gray_xyz.T, white_xyz)

    delta_xyz = np.zeros_like(gray_xyz)
    delta_xyz[1, :] = white_xyz[1] / 20.0
    lab2 = xyz_to_lab((gray_xyz + delta_xyz).T, white_xyz)

    delta_e = delta_e_ab(lab1, lab2)

    return lab1[:, 0], delta_e


if __name__ == "__main__":
    main()
