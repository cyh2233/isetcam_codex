import numpy as np
import matplotlib.pyplot as plt
from numpy.fft import fft2, fftshift
from isetcam.optics import wvf_zernike, wvf_mtf


def main():
    """Compute PSF and MTF from a simple Zernike wavefront."""
    n = 64
    x = np.linspace(-1, 1, n)
    X, Y = np.meshgrid(x, x)
    R = np.sqrt(X ** 2 + Y ** 2)
    T = np.arctan2(Y, X)

    # Simple combination of Zernike terms (j=2,3,4)
    coeffs = np.array([0.0, 0.1, -0.1, 0.05])
    wvf = wvf_zernike(coeffs, R, T)
    wvf[R > 1] = 0.0

    pupil = (R <= 1) * np.exp(2j * np.pi * wvf)
    psf = np.abs(fftshift(fft2(pupil))) ** 2
    psf /= psf.sum()
    mtf = wvf_mtf(psf)

    fig, axs = plt.subplots(1, 3, figsize=(9, 3))
    im0 = axs[0].imshow(wvf, extent=[-1, 1, -1, 1], cmap="jet")
    axs[0].set_title("Wavefront")
    axs[0].axis("off")
    fig.colorbar(im0, ax=axs[0])
    axs[1].imshow(psf, cmap="magma")
    axs[1].set_title("PSF")
    axs[1].axis("off")
    axs[2].imshow(mtf, cmap="magma")
    axs[2].set_title("MTF")
    axs[2].axis("off")
    fig.tight_layout()
    plt.close(fig)

    return wvf.shape, psf.shape, mtf.shape


if __name__ == "__main__":
    main()
