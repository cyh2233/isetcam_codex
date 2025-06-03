import numpy as np
from isetcam.optics import optics_airy_psf


def main():
    """Generate an Airy disk PSF and return basic properties."""
    psf = optics_airy_psf(64, 8.0)
    return psf.shape, float(psf.sum()), float(psf.max())


if __name__ == "__main__":
    main()
