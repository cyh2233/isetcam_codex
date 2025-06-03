import scipy.io
from isetcam.ip import ip_jpeg_compress, ip_jpeg_decompress


def main():
    mat = scipy.io.loadmat("scripts/image/jpegFiles/einstein.mat")
    im = mat["X"]
    coef = ip_jpeg_compress(im, 50)
    recon = ip_jpeg_decompress(coef)
    return im.shape, coef.shape, recon.shape


if __name__ == "__main__":
    main()
