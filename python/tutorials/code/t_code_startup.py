import sys
from isetcam.iset_root_path import iset_root_path


def main():
    """Show basic path setup for ISETCam."""
    root = iset_root_path()
    before = root in sys.path
    if not before:
        sys.path.append(root)
    after = root in sys.path
    return before, after, root


if __name__ == "__main__":
    main()
