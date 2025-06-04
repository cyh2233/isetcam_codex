from isetcam import ie_init
from isetcam.scene import scene_create
from isetcam.vc_add_and_select_object import vcSESSION
from isetcam import vc_add_and_select_object, vc_get_object


def main():
    """Demonstrate vcSESSION database management."""
    ie_init()

    before = len(vcSESSION.get("SCENE", []))

    scene = scene_create("macbeth d65")
    idx = vc_add_and_select_object("scene", scene)
    after = len(vcSESSION.get("SCENE", []))

    stored = vc_get_object("scene", idx)

    idx2 = vc_add_and_select_object("scene", scene)
    final = len(vcSESSION.get("SCENE", []))

    return (before, after, final), stored.photons.shape


if __name__ == "__main__":
    main()
