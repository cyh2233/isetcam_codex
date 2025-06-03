import numpy as np
from isetcam import ie_init
from isetcam.metrics import sensor_sqr_i


def main():
    """Compute the SQRI value for a simple display."""
    ie_init()

    n_sf = 1000
    sf = np.logspace(-1.5, 1.6, n_sf)
    d_mtf = np.ones_like(sf)
    luminance = 100.0
    width = 14.0

    sqri, hcsf = sensor_sqr_i(sf, d_mtf, luminance, width=width)

    return sqri, hcsf


if __name__ == "__main__":
    main()
