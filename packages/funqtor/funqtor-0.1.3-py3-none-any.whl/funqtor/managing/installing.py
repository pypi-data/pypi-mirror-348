import tomlkit as toml
import pathlib
import os
from enum import Enum
from ..helpers import qbprojectpath_helper

class Action(Enum):
    """Action to perform on the package."""
    ADD = "add"
    REMOVE = "remove"

def install_dependencies(path: pathlib.Path):
    """Install all dependencies."""

    venv_path = path / ".venv"
    qbproject_filepath = qbprojectpath_helper(path)
    old_qbproject_filepath = path / "qbproject.old.toml"

    if not qbproject_filepath:
        return

    if not venv_path.exists():
        print(f"Virtual environment not found at {venv_path}")
        return

    with open(qbproject_filepath, "r") as f:
        qbproject_data = toml.load(f)

    # Gathering dependencies from prior installation
    if old_qbproject_filepath.exists():
        with open(old_qbproject_filepath, "r") as f:
            old_qbproject_data = toml.load(f)

        old_dependencies = old_qbproject_data.get("project").get("dependencies", [])

    else:
        old_dependencies = []

    dependencies = qbproject_data.get("project").get("dependencies", [])
    redundant = list(set(old_dependencies) - set(dependencies))
    updated = list(set(dependencies) - set(old_dependencies))

    if len(dependencies) == 0:
        print("No dependencies found in qbproject.toml.")
        return

    if len(redundant) > 0:
        print(f"Uninstalling {len(redundant)} redundant dependencies: {', '.join(redundant)}")
        pip(venv_path, redundant, uninstall=True)
        print("Redundant dependencies uninstalled.")

    if len(updated) > 0:
        print(f"Installing {len(updated)} dependencies: {', '.join(updated)}")
        pip(venv_path, updated)
        print("Dependencies installed.")

    if not len(redundant) and not len(updated):
        print("No changes made, skipping.")

    with open(old_qbproject_filepath, "w") as f:
        toml.dump(qbproject_data, f)


def pip(venv_path: pathlib.Path, packages=None, uninstall=False, no_deps=False, force_update=False):
    """Pip wrapper for installing and uninstalling packages."""

    if packages is None:
        packages = []

    pip = venv_path / "Scripts" / "pip" if os.name == "nt" else venv_path / "bin" / "pip"

    if len(packages) == 0:
        print("No packages to install.")
        return

    args = [
        "install" if not uninstall else "uninstall",
        "--disable-pip-version-check",
        "--isolated",
        "--no-input" if not uninstall else "--yes",
        "--no-deps" if no_deps else "",
        "--force-reinstall" if force_update else "",
    ]

    args += packages

    os.system(f"{pip} {' '.join(args)}")


def modify(path: pathlib.Path, packages: str, action: Action):
    """Adds or removes packages from the qbproject.toml file."""
    qbproject_filepath = qbprojectpath_helper(path)

    if not qbproject_filepath:
        return

    with open(qbproject_filepath, "r") as f:
        qbproject_data = toml.load(f)

    dependencies = qbproject_data.get("project").get("dependencies", [])

    match action:
        case Action.ADD:
            added = []

            for package in packages:
                if package in dependencies:
                    print(f"Package {package} already exists in qbproject.toml.")
                    continue

                added.append(package)

                dependencies.append(package)

            print(f"Package(s) {', '.join(packages)} added to qbproject.toml." if added else "No packages added.")

        case Action.REMOVE:
            removed = []

            for package in packages:
                if package not in dependencies:
                    print(f"Package {package} not found in qbproject.toml.")
                    continue

                removed.append(package)

                dependencies.remove(package)

            print(f"Package(s) {', '.join(removed)} removed from qbproject.toml." if removed else "No packages removed.")

    qbproject_data["project"]["dependencies"] = dependencies

    with open(qbproject_filepath, "w") as f:
        toml.dump(qbproject_data, f)

def get_dependencies(path: pathlib.Path):
    """List all dependencies in the qbproject.toml file."""
    qbproject_filepath = qbprojectpath_helper(path)

    if not qbproject_filepath:
        return

    with open(qbproject_filepath, "r") as f:
        qbproject_data = toml.load(f)

    dependencies = qbproject_data.get("project").get("dependencies", [])
    return dependencies