from isetcam import ie_init
from isetcam.scene import scene_create
from isetcam import vc_add_and_select_object, vc_get_object


def main():
    """Demonstrate adding and retrieving objects from vcSESSION."""
    ie_init()

    # Create a simple scene and store it
    scene = scene_create("macbeth d65")
    idx = vc_add_and_select_object("scene", scene)

    # Retrieve the stored scene
    stored = vc_get_object("scene", idx)

    return idx, stored.photons.shape


if __name__ == "__main__":
    main()
