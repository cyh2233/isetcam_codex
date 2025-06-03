import numpy as np
import matplotlib.pyplot as plt
from isetcam import (
    ie_init,
    data_path,
    ie_read_spectra,
    ie_xyz_from_energy,
    lrgb_to_srgb,
)
from isetcam.display import display_create, display_set


def main():
    ie_init()

    wave = np.arange(400, 701, 10)
    XYZ, _, _, _ = ie_read_spectra(data_path("human/XYZ.mat"), wave)

    disp = display_create("LCD-Apple")
    spd = np.column_stack([
        np.interp(wave, disp.wave, disp.spd[:, i], left=0.0, right=0.0)
        for i in range(3)
    ])
    display_set(disp, "wave", wave)
    display_set(disp, "spd", spd)

    rgb2xyz = XYZ.T @ spd
    xyz2rgb = np.linalg.inv(rgb2xyz)

    d65_energy, _, _, _ = ie_read_spectra(data_path("lights/D65.mat"), wave)
    d65_energy = d65_energy.ravel()
    xyz = ie_xyz_from_energy(d65_energy[np.newaxis, :], wave).ravel()
    rgb = xyz2rgb @ xyz
    rgb = np.clip(rgb / rgb.max(), 0.0, 1.0)
    srgb = lrgb_to_srgb(rgb[np.newaxis, :]).ravel()

    plt.figure()
    plt.imshow(np.ones((10, 10, 3)) * srgb[np.newaxis, np.newaxis, :])
    plt.axis("off")

    return rgb2xyz, xyz2rgb, srgb


if __name__ == "__main__":
    main()
