import numpy as np
from isetcam import ie_init
from isetcam.printing import halftone_dither, halftone_error_diffusion


def main():
    """Demonstrate basic halftoning using dithering and error diffusion."""
    ie_init()

    # Clustered-dot halftone cell (4x4)
    half_tone_cell_4 = np.array(
        [
            [15, 5, 12, 14],
            [10, 3, 2, 8],
            [7, 1, 4, 11],
            [13, 9, 6, 16],
        ],
        dtype=float,
    )

    # Create an 8 strip grayscale sweep
    sweep_size = 64
    gray_strips = 8
    x, y = np.meshgrid(np.arange(sweep_size), np.arange(sweep_size))
    y = np.floor(y * gray_strips / sweep_size) / gray_strips
    x = x / (sweep_size * gray_strips)
    sweep = 1.0 - (x + y)

    monitor_gamma = 2.0
    sweep_linear = sweep ** monitor_gamma

    ht_dither = halftone_dither(half_tone_cell_4, sweep_linear)

    fs_matrix = np.array(
        [
            [0, 0, 0, 7, 5],
            [3, 5, 7, 5, 3],
            [1, 3, 5, 3, 1],
        ],
        dtype=float,
    )
    fs_matrix /= fs_matrix.sum()

    ht_error = halftone_error_diffusion(fs_matrix, sweep_linear)

    return ht_dither, ht_error


if __name__ == "__main__":
    main()
