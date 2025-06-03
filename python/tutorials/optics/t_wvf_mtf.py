import numpy as np
from isetcam.optics import optics_airy_psf, wvf_mtf


def main():
    """Compute the MTF of an Airy PSF."""
    psf = optics_airy_psf(64, 8.0)
    mtf = wvf_mtf(psf)
    center = mtf[psf.shape[0] // 2, psf.shape[1] // 2]
    return mtf.shape, float(center)


if __name__ == "__main__":
    main()
