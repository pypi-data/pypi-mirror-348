from importlib.metadata import requires

import tomlkit as toml
import pathlib
import os

def generate_qbproject(path: pathlib.Path):
    """
    Generates a sample qbproject.toml file in the specified path.
    """
    git_username = os.popen("git config --get user.name").read().strip() or ""
    git_email = os.popen("git config --get user.email").read().strip() or ""
    python_version = os.popen("python --version").read().strip().split()[1] or ""

    qbproject_data = {
        "project": {
            "name": path.name,
            "version": "0.1.0",
            "description": "",
            "authors": toml.array(),

            "requires_python": f">={python_version}",

            "dependencies": [
                "qb-runtime"
            ]
        },

        "build-system": {
            "requires": ["hatchling >= 1.27"],
            "build-backend": "hatchling.build"
        }
    }

    t = toml.inline_table()

    t.update({"name": git_username, "email": git_email})

    qbproject_data["project"]["authors"].append(t)


    toml_filepath = path / "qbproject.toml"

    if toml_filepath.exists():
        print(f"File {toml_filepath} already exists.")
        return

    with open(toml_filepath, "w") as f:
        toml.dump(qbproject_data, f)

    print(f"qbproject.toml created at {toml_filepath}.")


def generate_gitignore(path: pathlib.Path):
    gitignore_path = path / ".gitignore"

    if gitignore_path.exists():
        print(f"File {gitignore_path} already exists.")
        return

    ignore = [".venv/", "build/"]
    with open(gitignore_path, "w") as f:
        f.write("\n".join(ignore))

    print(f".gitignore created at {gitignore_path}.")