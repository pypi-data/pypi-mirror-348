import pathlib
import os

from enum import Enum
from dotenv import load_dotenv, set_key
from requests import HTTPError
from twine.commands import upload as twine_upload


def set_pypi_key(path: pathlib.Path, value: str = None):
    """Set the credentials for the publisher"""
    dotenv_path = path / "pypi.env"

    if not dotenv_path.exists():
        dotenv_path.touch()

    load_dotenv(dotenv_path)

    if value is None:
        value = input("Enter your PyPI-API-Token: ")

    set_key(dotenv_path, "PYPI_KEY", value)


def get_key(path: pathlib.Path):
    """Get the credentials for the publisher"""
    dotenv_path = path / "pypi.env"

    if not dotenv_path.exists():
        dotenv_path.touch()

    load_dotenv(dotenv_path, override=True)

    return os.getenv("PYPI_KEY")


def upload(path: pathlib.Path, test: bool = False):
    """Upload the package to PyPI"""
    packaged_path = path / "build" / "packaged"
    dotenv_path = path / "pypi.env"

    if not dotenv_path.exists():
        print("Credentials not set. Please run 'quasar setkey' first.")
        return

    password = get_key(path)

    if not password:
        print("Credentials not set. Please run 'quasar setkey' first.")
        return

    if not packaged_path.exists():
        print("Packaged directory does not exist. Please run 'quasar package' first or supply 'build' as an argument.")
        return

    args = [
        str(packaged_path / "*"),
        f"-p {password}",
        "--non-interactive",
    ]

    if test:
        args.append("--repository-url=https://test.pypi.org/legacy/")

    try:
        twine_upload.main(args)

    except HTTPError as e:
        print(f"Error uploading package: {e}")
        return