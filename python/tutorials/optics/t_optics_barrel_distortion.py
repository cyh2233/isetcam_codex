import numpy as np
from isetcam.optics import optics_barrel_distortion


def main():
    """Apply barrel distortion to unit circle points."""
    x = np.array([1.0, 0.0])
    y = np.array([0.0, 1.0])
    xd, yd = optics_barrel_distortion(x, y, k1=-0.3)
    rin = np.hypot(x, y)
    rout = np.hypot(xd, yd)
    return rin, rout


if __name__ == "__main__":
    main()
