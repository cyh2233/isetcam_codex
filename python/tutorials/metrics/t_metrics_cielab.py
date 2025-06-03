import numpy as np
from isetcam import ie_init
from isetcam.metrics import delta_e_ab


def main():
    """Simple demonstration of DeltaE calculations."""
    ie_init()

    lab1 = np.array([[50.0, 20.0, 30.0]])
    lab2 = np.array([[55.0, 22.0, 35.0]])

    de76 = float(delta_e_ab(lab1, lab2, version="1976"))
    de94 = float(delta_e_ab(lab1, lab2, version="94"))
    de2000 = float(delta_e_ab(lab1, lab2, version="2000"))

    return de76, de94, de2000


if __name__ == "__main__":
    main()
