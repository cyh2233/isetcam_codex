import numpy as np
import scipy.io
from isetcam.ip import ip_jpeg_compress, ip_jpeg_decompress


def main():
    mat = scipy.io.loadmat("scripts/image/jpegFiles/clown.mat")
    X = mat["X"]
    cmap = mat["map"]
    rgb = cmap[X.astype(int) - 1]

    r_coef = ip_jpeg_compress(rgb[:, :, 0], 75)
    g_coef = ip_jpeg_compress(rgb[:, :, 1], 75)
    b_coef = ip_jpeg_compress(rgb[:, :, 2], 75)

    r_jpeg = ip_jpeg_decompress(r_coef)
    g_jpeg = ip_jpeg_decompress(g_coef)
    b_jpeg = ip_jpeg_decompress(b_coef)
    rgb_jpeg = np.stack([r_jpeg, g_jpeg, b_jpeg], axis=2)
    return rgb.shape, rgb_jpeg.shape


if __name__ == "__main__":
    main()
