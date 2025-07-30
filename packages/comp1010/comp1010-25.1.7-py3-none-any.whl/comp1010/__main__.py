"""
# COMP1010 Metapackage

This library includes all required COMP1010 dependencies, as well as a simple
utility to display helpful debug information.
"""

import json
from os import uname
from sys import executable
from sys import version_info as version

from colorama import Fore
from subtask import Subtask

from comp1010 import __version__

IMPORTANT_PACKAGES = ["pyhtml-enhanced", "pyhtml", "Flask"]
"""
Packages that tutors probably want to know the version of if debugging a setup
"""


BLUE = Fore.BLUE
GREEN = Fore.GREEN
RED = Fore.RED
YELLOW = Fore.YELLOW
RESET = Fore.RESET


RAINBOW = [
    Fore.RED,
    Fore.YELLOW,
    Fore.GREEN,
    Fore.CYAN,
    Fore.BLUE,
    Fore.MAGENTA,
]


def rainbow(text: str) -> str:
    """Rainbow text"""
    return (
        "".join(f"{RAINBOW[i % len(RAINBOW)]}{c}" for i, c in enumerate(text))
        + f"{RESET}"
    )


def get_packages_info() -> dict[str, str]:
    """
    Return package info as a mapping between packages and their versions.
    """
    pip = Subtask([executable, "-m", "pip", "list", "--format", "json"])
    pip.wait()
    packages = json.loads(pip.read_stdout())

    return {package["name"]: package["version"] for package in packages}


def main():
    python_version = f"{version.major}.{version.minor}.{version.micro}"
    print(rainbow("===================="))
    print("COMP1010 Metapackage")
    print(f"{BLUE}v{__version__}{RESET}")
    print(rainbow("===================="))
    print()
    print(f"Python version: {BLUE}{python_version}{RESET}")
    print(f"OS: {BLUE}{uname().sysname} {uname().release}{RESET}")
    print()
    print("Core package versions:")
    print(f"{YELLOW}  Don't stress if some are not installed. This is just")
    print("  displayed in case your tutor needs to help you out!")
    print(RESET)

    installed = get_packages_info()

    for package in IMPORTANT_PACKAGES:
        if package in installed:
            package_version = f"{GREEN} {installed[package]}"
        else:
            package_version = f"{RED} Not installed"

        print(f"{package.ljust(20)}{package_version} {RESET}")


if __name__ == "__main__":
    main()
