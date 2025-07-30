
from importlib import resources
import json
import os
from pathlib import Path
import sys
from typing import Optional
import tree_structure

def show_available_config():
    config_dir = resources.files("aidge_core.benchmark.operator_config")
    config_files = [f for f in config_dir.iterdir() if f.is_file() and (f.suffix == ".json")]
    nb_files = len(config_files)
    tree = tree_structure.TreeStruct()
    print("Available configuration files")
    for i, cf in enumerate(config_files):
        print(f"{tree.grow(False, i >= nb_files - 1)} {cf.name}")


def find_file_in_package(file_path: str) -> Optional[str]:
    """Try to locate the given config file either in current directory or in package data."""
    # Try loading from packaged resources
    try:
        config_file = resources.files("aidge_core.benchmark.operator_config").joinpath(file_path)
        if config_file.is_file():
            return config_file
    except ModuleNotFoundError:
        pass  # if resources can't find the package

    # Not found
    return None

def load_json(file_path: str, search_dir: str = '.') -> dict:
    """
    Loads and returns the JSON configuration from the given file.
    Searches in the given directory, current working directory, and package resources.
    """
    config_path = None

    file_path_obj = Path(file_path)
    search_dir_path = Path(os.path.expanduser(search_dir))

    # Check if file_path is directly usable
    if file_path_obj.is_file():
        config_path = file_path_obj
    # Check inside the search_dir
    elif (search_dir_path / file_path_obj).is_file():
        config_path = search_dir_path / file_path_obj
    # Fallback to package search
    elif find_file_in_package(file_path):
        config_path = find_file_in_package(file_path)

    if not config_path:
        print(file_path, search_dir, file_path_obj, search_dir_path)
        print("Cannot find JSON file.")
        sys.exit(1)

    with open(config_path, "r") as f:
        return json.load(f)