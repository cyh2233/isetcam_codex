import numpy as np
from isetcam.optics import optics_fresnel


def main():
    """Propagate a delta function field using Fresnel approximation."""
    field = np.zeros((32, 32), dtype=complex)
    field[16, 16] = 1.0
    out = optics_fresnel(field, dx=1e-6, wavelength=500e-9, distance=0.01)
    energy_in = float(np.sum(np.abs(field) ** 2))
    energy_out = float(np.sum(np.abs(out) ** 2))
    return energy_in, energy_out, out.shape


if __name__ == "__main__":
    main()
