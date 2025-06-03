import numpy as np
from isetcam.optics import wvf_zernike


def main():
    """Evaluate a wavefront from a single Zernike coefficient."""
    rho = np.linspace(0, 1, 10)
    theta = np.linspace(0, 2 * np.pi, 10, endpoint=False)
    R, T = np.meshgrid(rho, theta)
    coeffs = np.array([1.0])
    wvf = wvf_zernike(coeffs, R, T)
    return wvf.shape, float(wvf.mean())


if __name__ == "__main__":
    main()
