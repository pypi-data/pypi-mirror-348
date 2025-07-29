import pathlib

from ..building import get_build_directory
from ..managing import pip
from build.__main__ import main as build_main


def package(path: pathlib.Path):
    build_directory = get_build_directory(path)
    packaged_directory = build_directory.parent / "packaged"

    args = [
        str(build_directory),
        "--outdir",
        str(packaged_directory),
    ]

    if not packaged_directory.exists():
        packaged_directory.mkdir(parents=True, exist_ok=True)

    build_main(args)


def install_self(path: pathlib.Path):
    build_directory = get_build_directory(path)
    packaged_directory = build_directory.parent / "packaged"

    wheels = []

    for file in packaged_directory.iterdir():
        if file.suffix == ".whl":
            wheels.append(str(file))

    venv_path = path / ".venv"

    pip(venv_path, wheels, no_deps=True, force_update=True)