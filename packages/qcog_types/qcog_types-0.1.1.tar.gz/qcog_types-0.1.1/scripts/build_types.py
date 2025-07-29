import os
import pathlib
import shutil

default_include = [
    "hyperparameters.py",
    "__init__.py",
]

exclude_folders = [
    ".venv",
    ".git",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".vscode",
    "qcogtypes.egg-info",
    "__pycache__",
    "qcog_exp.egg-info",
]

packages = [
    "intech"
]

def continue_walk(path: pathlib.Path) -> bool:
    # Check if the path contains one of the `exclude_folders`
    for folder in exclude_folders:
        if folder in path.parts:
            return False
    return True

def build_types(
    *,
    include: list[str] | None = None,
):
    include = include or default_include
    ### Create the qcog_types folder
    qcog_types_dir = pathlib.Path(os.getcwd()) / "qcog_types"
    qcog_types_dir.mkdir(parents=True, exist_ok=True)

    try:
    ### Start from the root folder
        root = pathlib.Path(os.getcwd())

        qcog_exp_dir = root / "qcog_exp"

        def walk(path: pathlib.Path):
            folder = path.name
            print(".. -> folder ", folder)
            if folder in exclude_folders:
                return

            for current_path, dirnames, filenames in path.walk():
                if not continue_walk(current_path):
                    return

                print(" -> current_path ", current_path)

                for filename in filenames:
                    if filename in include:
                        # Build the directory mirroring the path
                        # Replace the qcog_exp prefix with qcog_types
                        print(".. File to copy found! ", filename)
                        types_path = pathlib.Path(str(current_path).replace("qcog_exp", "qcog_types"))
                        print(".. types_path ", types_path)
                        types_path.mkdir(parents=True, exist_ok=True)
                        # Copy the file to the types path
                        copied_path = shutil.copy(current_path / filename, types_path / filename)
                        print(f"{current_path} -> {copied_path}")

                for dirname in dirnames:
                    if dirname not in exclude_folders:
                        walk(current_path / dirname)

        walk(qcog_exp_dir)

    except Exception as e:
        print(e)
    finally:
        pass


if __name__ == "__main__":
    build_types()
