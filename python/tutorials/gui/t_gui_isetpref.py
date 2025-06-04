import argparse
import matplotlib.pyplot as plt
from isetcam import ie_init, ie_session_get, ie_session_set
from isetcam.scene import scene_create, scene_show_image


def _prompt(interactive: bool, msg: str):
    if interactive:
        input(msg)
    else:
        plt.pause(0.5)


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Demonstrate ISET preferences"
    )
    parser.add_argument(
        "--no-interactive",
        action="store_true",
        help="Run without prompts",
    )
    args = parser.parse_args(argv)
    interactive = not args.no_interactive

    ie_init()

    print("Waitbar:", ie_session_get("waitbar"))
    print("Font size:", ie_session_get("font size"))

    _prompt(interactive, "Enable waitbar and press Enter...")
    ie_session_set("waitbar", 1)
    print("Waitbar:", ie_session_get("waitbar"))

    _prompt(interactive, "Disable waitbar and press Enter...")
    ie_session_set("waitbar", 0)
    print("Waitbar:", ie_session_get("waitbar"))

    scene = scene_create("macbeth d65")
    ax = scene_show_image(scene)
    plt.show(block=False)

    _prompt(interactive, "Increase font size and press Enter...")
    size = ie_session_get("font size")
    ie_session_set("font size", size + 2)
    ax.set_title("Font size %d" % ie_session_get("font size"))
    ax.figure.canvas.draw()

    _prompt(interactive, "Restore font size and press Enter...")
    ie_session_set("font size", size)
    ax.set_title("Font size %d" % ie_session_get("font size"))
    ax.figure.canvas.draw()

    plt.close(ax.figure)
    return True


if __name__ == "__main__":
    main()
