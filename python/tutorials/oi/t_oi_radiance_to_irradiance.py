import numpy as np
from isetcam.opticalimage import oi_radiance_to_irradiance


def main():
    radiance = np.linspace(0.1, 1.0, 5)
    f_number = 4.0
    irradiance = oi_radiance_to_irradiance(radiance, f_number)
    return irradiance


if __name__ == "__main__":
    main()
