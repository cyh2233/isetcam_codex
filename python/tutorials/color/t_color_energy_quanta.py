import numpy as np
import matplotlib.pyplot as plt
from isetcam import (
    ie_init,
    data_path,
    ie_read_spectra,
    quanta_to_energy,
    energy_to_quanta,
    ie_xyz_from_energy,
    ie_xyz_from_photons,
    chromaticity,
)


def main():
    ie_init()

    wave = np.arange(400, 705, 5)

    photons = np.ones_like(wave)
    energy = quanta_to_energy(wave, photons).ravel()

    plt.figure()
    plt.plot(wave, energy)
    plt.xlabel("Wavelength (nm)")
    plt.ylabel("Energy (watts/sr/nm/m2)")
    plt.grid(True)

    d65_energy, _, _, _ = ie_read_spectra(data_path("lights/D65.mat"), wave)
    d65_xyz = ie_xyz_from_energy(d65_energy.T, wave).ravel()
    d65_energy = d65_energy.ravel() * 100 / d65_xyz[1]

    plt.figure()
    plt.plot(wave, d65_energy)
    plt.xlabel("Wavelength (nm)")
    plt.ylabel("Energy (watts/sr/nm/m2)")
    plt.grid(True)

    d65_photons = energy_to_quanta(wave, d65_energy).ravel()
    plt.figure()
    plt.plot(wave, d65_photons)
    plt.xlabel("Wavelength (nm)")
    plt.ylabel("Photons (q/sr/nm/m2)")
    plt.grid(True)

    xyz_energy, _, _, _ = ie_read_spectra(data_path("human/XYZ.mat"), wave)
    xyz_quanta = energy_to_quanta(wave, xyz_energy)

    plt.figure()
    plt.plot(wave, xyz_energy)
    plt.title("XYZ standard (energy)")
    plt.grid(True)

    plt.figure()
    plt.plot(wave, xyz_quanta)
    plt.title("XYZ photons")
    plt.grid(True)

    d65_xyz_p = ie_xyz_from_photons(d65_photons, wave).ravel()
    d65_xyz_e = ie_xyz_from_energy(d65_energy, wave).ravel()

    _ = (d65_xyz_p, d65_xyz_e, chromaticity(d65_xyz_e[np.newaxis, :]))

    return energy, d65_energy, d65_photons, xyz_energy, xyz_quanta


if __name__ == "__main__":
    main()
