from os.path import expanduser
from pathlib import Path
from typing import Optional, Union

from dotenv import dotenv_values, find_dotenv


def config_to_bool(config_value: Optional[str]):
    """Turn a config value into a bool."""
    if not config_value or config_value.lower() in ["false", "0", "no"]:
        return False
    else:
        assert config_value.lower() in [
            "true",
            1,
            "yes",
        ], f"Invalid boolean config value: {config_value}"
        return True


def load_config():
    """Load the configuration files and convert known values"""
    config_dict: dict[str, Union[None, str, int, Path]] = {
        **dotenv_values(find_dotenv(".env")),
        **dotenv_values(find_dotenv(".env.local")),
    }

    bool_config_values = ["remove_duplicate_bi_encoder_results"]
    integer_config_values = [
        "num_processes",
        "top_k",
        "batch_size",
        "max_paragraphs_per_page",
        "max_sentences_per_paragraph",
    ]
    path_config_values = ["data_path", "crawl_result_file"]

    for key in bool_config_values:
        config_dict[key] = config_to_bool(config_dict[key])
    for key in integer_config_values:
        config_dict[key] = int(config_dict[key])
    for key in path_config_values:
        config_dict[key] = Path(expanduser(config_dict[key]))
    return config_dict
