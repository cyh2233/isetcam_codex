import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from isetcam import (
    ie_init,
    data_path,
    ie_read_spectra,
    lrgb_to_srgb,
)
from isetcam.display import display_create, display_set


def main():
    ie_init()

    wave = np.arange(390, 731)
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

    rgb_spectrum = (xyz2rgb @ XYZ.T).T

    Yvalue = XYZ[:, 1]
    scale_factor = Yvalue + 0.4
    rgb_spectrum = rgb_spectrum / scale_factor[:, np.newaxis]

    gray_level = abs(rgb_spectrum.min())
    rgb_spectrum = rgb_spectrum + gray_level
    rgb_spectrum = rgb_spectrum / rgb_spectrum.max()

    plt.figure()
    plt.plot(wave, rgb_spectrum)
    plt.xlabel("Wavelength (nm)")
    plt.ylabel("Linear RGB")
    plt.grid(True)

    srgb = lrgb_to_srgb(rgb_spectrum)

    cmap = ListedColormap(srgb)
    plt.figure()
    plt.imshow(np.arange(len(wave))[np.newaxis, :], cmap=cmap, aspect="auto")
    plt.xlabel("wavelength (nm)")

    return rgb_spectrum, srgb


if __name__ == "__main__":
    main()
