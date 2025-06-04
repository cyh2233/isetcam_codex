import argparse
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
import numpy as np


def _prompt(interactive: bool):
    if interactive:
        input("Press Enter to continue...")
    else:
        plt.pause(0.5)


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Draw ROI shapes on sample images"
    )
    parser.add_argument(
        "--no-interactive",
        action="store_true",
        help="Skip prompts and close immediately",
    )
    args = parser.parse_args(argv)
    interactive = not args.no_interactive

    fig, axs = plt.subplots(2, 2, figsize=(6, 6))
    titles = ["Scene", "Optical Image", "Sensor", "IP"]
    for ax, title in zip(axs.ravel(), titles):
        ax.imshow(np.zeros((100, 100, 3)))
        ax.set_title(title)
        ax.axis("off")
    fig.tight_layout()
    plt.show(block=False)

    rect = Rectangle(
        (50, 20),
        10,
        5,
        linewidth=5,
        edgecolor="r",
        facecolor="none",
        linestyle=":",
    )
    axs[0, 0].add_patch(rect)
    _prompt(interactive)
    rect.remove()

    rect = Rectangle(
        (50, 50),
        20,
        20,
        linewidth=2,
        edgecolor="w",
        facecolor="none",
        linestyle=":",
    )
    axs[0, 1].add_patch(rect)
    _prompt(interactive)
    rect.remove()

    circ = Circle((30, 15), 20, edgecolor="w", facecolor="none")
    axs[0, 1].add_patch(circ)
    _prompt(interactive)
    circ.remove()

    circ = Circle((20, 20), 10, edgecolor="w", facecolor="none")
    axs[1, 0].add_patch(circ)
    _prompt(interactive)
    circ.remove()

    rect = Rectangle((50, 50), 20, 20, edgecolor="g", facecolor="none")
    axs[1, 1].add_patch(rect)
    _prompt(interactive)
    rect.remove()

    plt.close(fig)
    return True


if __name__ == "__main__":
    main()
