import numpy as np
from isetcam import ie_init
from isetcam.scene import (
    scene_create,
    scene_show_image,
    scene_plot,
    scene_adjust_illuminant,
    scene_description,
)
from isetcam.illuminant import illuminant_blackbody


def main() -> None:
    ie_init()

    # Create a simple Macbeth chart scene and display it
    scene = scene_create("macbeth d65")
    scene.fov = 8.0
    scene_show_image(scene)

    # Print a short text description of the scene
    print(scene_description(scene))

    # Plot the radiance image
    scene_plot(scene, kind="radiance image")

    # Change some scene parameters
    scene.distance = 0.6
    scene.fov /= 2.0

    # Adjust the illuminant to a 5500 K blackbody
    bb = illuminant_blackbody(5500, scene.wave)
    scene = scene_adjust_illuminant(scene, bb)
    scene_show_image(scene)


if __name__ == "__main__":
    main()
