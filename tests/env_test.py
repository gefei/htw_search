from pathlib import Path

from htw_search.utils import env


def test_boolean_config_values():
    config = env.load_config()
    assert type(config["remove_duplicate_bi_encoder_results"]) == bool


def test_int_config_values():
    config = env.load_config()
    assert isinstance(config["num_processes"], int)
    assert isinstance(config["top_k"], int)
    assert isinstance(config["max_paragraphs_per_page"], int)
    assert isinstance(config["max_sentences_per_paragraph"], int)


def test_path_config_values():
    config = env.load_config()
    assert isinstance(config["data_path"], Path)
    assert config["data_path"].exists()
    assert isinstance(config["crawl_result_file"], Path)
