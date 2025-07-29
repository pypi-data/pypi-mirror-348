import sys
from pathlib import Path

from qb_quasar.building import build_project, run, qbprojectpath_helper
from qb_quasar.initializing import init
from qb_quasar.managing import install_dependencies, modify, Action, get_dependencies
from qb_quasar.packaging import package, install_self, set_pypi_key, upload

def main(args=None):
    if args is None:
        args = sys.argv[1:] or ["help"]

    command = args[0]

    cwd = Path.cwd()
    program = Path(sys.argv[0]).name.split(".")[0]

    match command:
        case "init":
            path = Path(args[1]) if len(args) > 1 else None
            init(path)

        case "help":
            commands = {
                "init": "Initialize a new qbquasar project.",
                "install [self]": "Install dependencies. If 'self' is provided, install the package itself along with its dependencies.",
                "add": "Add packages to the qbproject.toml file.",
                "remove": "Remove packages from the qbproject.toml file.",
                "list": "List all dependencies in the qbproject.toml file.",
                "build": "Build the project.",
                "run": "Run a command from the project environment.",
                "package": "Package the project for distribution.",
                "setkey": "Set the PyPI API key for publishing.",
                "publish [test] [build]": "Publish the package to PyPI. If 'test' is provided, publish to TestPyPI. If 'build' is provided, build the project before publishing.",
            }

            print("Available commands:")
            for cmd, desc in commands.items():
                print(f"  - {program} {cmd}: {desc}")
            return

        case "install":
            toml_existence_check(cwd)

            install_dependencies(cwd)

            if "self" in args[1:]:
                build_project(cwd)
                package(cwd)
                install_self(cwd)
                return

        case "add":
            toml_existence_check(cwd)

            packages = args[1:] if len(args) > 1 else None

            if not packages:
                print("Please provide a package name.")
                return

            modify(cwd, packages, Action.ADD)
            install_dependencies(cwd)

        case "remove":
            toml_existence_check(cwd)

            packages = args[1:] if len(args) > 1 else None

            if not packages:
                print("Please provide a package name.")
                return

            modify(cwd, packages, Action.REMOVE)
            install_dependencies(cwd)

        case "list":
            toml_existence_check(cwd)

            dependencies = get_dependencies(cwd)

            if dependencies:
                print("Installed packages:")
                for dep in dependencies:
                    print(f"  - {dep}")

            else:
                print("No dependencies found.")
                return

        case "build":
            toml_existence_check(cwd)

            clean = "clean" in args[1:]
            build_project(cwd, clean)

        case "run":
            toml_existence_check(cwd)

            command = args[1:] if len(args) > 1 else []
            run(cwd, command)

        case "package":
            toml_existence_check(cwd)

            build_project(cwd)
            package(cwd)

        case "setkey":
            toml_existence_check(cwd)

            value = args[1] if len(args) > 1 else None

            set_pypi_key(cwd, value)


        case "publish":
            toml_existence_check(cwd)

            test = "test" in args[1:]
            build = "build" in args[1:]

            if build:
                build_project(cwd, clean=True)
                package(cwd)

            upload(cwd, test)

        case _:
            return main(["help"])


def toml_existence_check(cwd):
    if not qbprojectpath_helper(cwd):
        print(f"qbproject.toml not found in {cwd}.")
        exit(1)