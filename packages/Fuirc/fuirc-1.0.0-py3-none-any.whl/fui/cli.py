import subprocess
import sys

import fui.version
from fui.utils.pip import ensure_fui_cli_package_installed


def main():
    ensure_fui_cli_package_installed()
    import fui_cli.cli

    fui_cli.cli.main()


if __name__ == "__main__":
    main()
