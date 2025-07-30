import subprocess
import sys

import fui.version


def install_fui_package(name: str):
    print(f"Installing {name} {fui.version.version} package...", end="")
    retcode = subprocess.call(
        [
            sys.executable,
            "-m",
            "pip",
            "install",
            "-q",
            "--disable-pip-version-check",
            f"{name}=={fui.version.version}",
        ]
    )
    if retcode == 0:
        print("OK")
    else:
        print(
            f'Unable to upgrade "{name}" package to version {fui.version.version}. Please use "pip install \'fui[all]=={fui.version.version}\' --upgrade" command to upgrade fui.'
        )
        exit(1)


def ensure_fui_desktop_package_installed():
    try:
        import fui.version
        import fui_desktop.version

        assert (
            not fui_desktop.version.version
            or fui_desktop.version.version == fui.version.version
        )
    except:
        install_fui_package("fui-desktop")


def ensure_fui_web_package_installed():
    try:
        import fui.version
        import fui_web.version

        assert (
            not fui_web.version.version
            or fui_web.version.version == fui.version.version
        )
    except:
        install_fui_package("fui-web")


def ensure_fui_cli_package_installed():
    try:
        import fui.version
        import fui_cli.version

        assert (
            not fui_cli.version.version
            or fui_cli.version.version == fui.version.version
        )
    except:
        install_fui_package("fui-cli")
