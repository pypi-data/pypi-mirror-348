import os
import pathlib
from .managing import generate_qbproject, generate_gitignore
from .managing import install_dependencies

def init(path: pathlib.Path = None):
    """Initialize a package."""
    if path is None:
        path = pathlib.Path.cwd()

        if len(os.listdir(path)) > 0:
            print("Current directory is not empty. This may cause issues.")

    else:
        if not path.exists():
            os.makedirs(path)

        else:
            print(f"Path {path} already exists.")
            return

    generate_qbproject(path)
    generate_gitignore(path)
    setup_venv(path)
    install_dependencies(path)
    create_module_alpha(path)


def setup_venv(path: pathlib.Path):
    """Set up a virtual environment."""

    venv_path = path / ".venv"

    if not venv_path.exists():
        os.system(f"python -m venv {venv_path}")
        print(f"Virtual environment created at {venv_path}")

    else:
        print(f"Virtual environment already exists at {venv_path}")

def create_module_alpha(path: pathlib.Path):
    """Creates a simple directory structure for the programmer"""
    module_alpha = path / "src" / path.name
    init_qb = module_alpha / "__init__.qb"

    if not module_alpha.exists():
        os.makedirs(module_alpha)

    if not init_qb.exists():
        with open(init_qb, "w") as f:
            pass