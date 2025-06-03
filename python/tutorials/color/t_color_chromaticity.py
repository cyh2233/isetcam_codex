import numpy as np
import matplotlib.pyplot as plt
from isetcam import (
    ie_init,
    chromaticity,
    chromaticity_plot,
    ie_xyz_from_energy,
    ie_xyz_from_photons,
)
from isetcam.display import display_create, display_plot
from isetcam.scene import scene_create


def main():
    ie_init()

    disp = display_create("lcdExample")
    display_plot(disp, kind="gamut")

    xy_white = chromaticity(disp.white_point[np.newaxis, :])[0]
    chromaticity_plot(xy_white[np.newaxis, :])

    xyz_primaries = ie_xyz_from_energy(disp.spd.T, disp.wave)
    xy_primaries = chromaticity(xyz_primaries)
    chromaticity_plot(xy_primaries)

    scene = scene_create("macbeth d65")
    xyz_scene = ie_xyz_from_photons(scene.photons, scene.wave)
    xy_scene = chromaticity(xyz_scene.reshape(-1, 3))
    chromaticity_plot(xy_scene)

    return xy_white, xy_primaries, xy_scene


if __name__ == "__main__":
    main()
