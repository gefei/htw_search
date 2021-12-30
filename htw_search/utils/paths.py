from pathlib import Path
from .env import load_config

_config = load_config()


def get_data_path(check_path_exists=True) -> Path:
    path = _config["data_path"]
    if check_path_exists:
        assert path.exists(), f"Data path {path} does not exist."
    return path


def get_path_for_crawl_result_file(check_path_exists=True) -> Path:
    path = _config["crawl_result_file"]
    if check_path_exists:
        assert path.exists(), f"Crawl result file {path} does not exist."
    return path


def get_path_for_pickle_file(file_name: str) -> Path:
    root_path = get_data_path(check_path_exists=True)
    pickle_path = root_path / "pickles"
    pickle_path.mkdir(exist_ok=True)
    return pickle_path / file_name
