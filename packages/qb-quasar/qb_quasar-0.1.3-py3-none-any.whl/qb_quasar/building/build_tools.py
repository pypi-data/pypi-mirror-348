import pathlib
import shutil
import tomlkit as toml

from ..helpers import qbprojectpath_helper
from .compiling import compile_to_qb


def build_project(path: pathlib.Path, clean: bool = False):
    """Builds the project by creating a build directory and copying the necessary files"""

    print("Building project", path.name)

    _ = get_build_directory(path, clean)
    translate_project_toml(path)
    copy_other_files(path)
    create_source_directories(path)

    for file in find_qb_files(path):
        write_compiled(path, file)

    print("Done")


def get_build_directory(path: pathlib.Path, clean: bool = False):
    """Sets up the build directory for the intermediary representation in Python"""
    intermediary_path = path / "build" / "intermediary"

    if not intermediary_path.exists():
        intermediary_path.mkdir(parents=True, exist_ok=True)

    else:
        if clean:
            shutil.rmtree(intermediary_path)

    return intermediary_path


def create_source_directories(path: pathlib.Path):
    """Creates the src and tests directories for the project"""
    build_directory = get_build_directory(path)

    src_directory = build_directory / "src"
    tests_directory = build_directory / "tests"

    if not src_directory.exists():
        src_directory.mkdir(parents=True, exist_ok=True)

    if not tests_directory.exists():
        tests_directory.mkdir(parents=True, exist_ok=True)


def translate_project_toml(path: pathlib.Path):
    qbproject_filepath = qbprojectpath_helper(path)

    if not qbproject_filepath:
        return

    build_directory = get_build_directory(path)

    with qbproject_filepath.open("r") as file:
        qbproject_data = toml.load(file)

    pyproject_filepath = build_directory / "pyproject.toml"

    with pyproject_filepath.open("w") as file:
        toml.dump(qbproject_data, file)


def copy_other_files(path: pathlib.Path):
    build_directory = get_build_directory(path)
    exclude = [
        ".gitignore",
        "qbproject.toml",
        "qbproject.old.toml",
        "src",
        "tests",
        "build",
        ".venv",
    ]

    for item in path.iterdir():
        if item.name in exclude:
            continue

        if item.is_dir():
            shutil.copytree(item, build_directory / item.name, dirs_exist_ok=True)
        else:
            shutil.copy(item, build_directory / item.name)


def find_qb_files(path: pathlib.Path):
    """Finds all qb files in the project directory, relative to the build directory"""
    qb_files = []

    for item in path.rglob("*.qb"):
        if item.is_file():
            qb_files.append(item.relative_to(path))

    return qb_files


def write_compiled(path: pathlib.Path, qb_file: pathlib.Path):
    """Writes the compiled code to the build directory"""
    build_directory = get_build_directory(path)
    destination = (build_directory / qb_file).with_suffix(".py")

    if not destination.parent.exists():
        destination.parent.mkdir(parents=True, exist_ok=True)

    code = read_qb_file(qb_file)

    with destination.open("w") as file:
        file.write(code)


def read_qb_file(qb_file: pathlib.Path):
    """Reads the qb file and returns the code"""

    with qb_file.open("r") as file:
        code = file.read()

    code = compile_to_qb(code)

    return code
