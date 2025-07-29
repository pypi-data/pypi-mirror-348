from pathlib import Path

def qbprojectpath_helper(path: Path):
    """Helper function to get the qbproject.toml path."""
    if path is None:
        path = Path.cwd()

    qbproject_filepath = path / "qbproject.toml"

    if not qbproject_filepath.exists():
        return None

    return qbproject_filepath