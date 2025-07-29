from pathlib import Path

def qbprojectpath_helper(path: Path):
    """Helper function to get the qbproject.toml path."""
    if path is None:
        path = Path.cwd()

    qbproject_filepath = path / "qbproject.toml"

    if not qbproject_filepath.exists():
        print(f"qbproject.toml not found at {qbproject_filepath}")
        return None

    return qbproject_filepath