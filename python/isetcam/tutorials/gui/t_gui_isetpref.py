from . import _run_tutorial
from typing import Sequence, Any


def main(argv: Sequence[str] | None = None) -> Any:
    return _run_tutorial("t_gui_isetpref", argv)


if __name__ == "__main__":
    main()
