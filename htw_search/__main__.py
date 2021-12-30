from pathlib import Path
import typer

from htw_search.utils.env import load_config
from htw_search.utils.paths import get_path_for_pickle_file

app = typer.Typer()
config = load_config()


@app.command()
def convert_crawl_data(
    path: Path = typer.Argument(
        config["crawl_result_file"], help="The path of the crawl file."
    )
):
    from htw_search.build_page_pickles import (
        parse_jsonl_file_from_crawl,
        save_pages_as_pickle,
    )

    print(f"Loading crawl file {path}...", end="")
    pages = parse_jsonl_file_from_crawl(path)
    print(f"done.\nFound {len(pages)} pages.\nSaving pages to file...", end="")
    save_pages_as_pickle(pages, get_path_for_pickle_file("pages.pkl"))
    print("done.")


@app.command()
def build_embeddings():
    from htw_search.build_page_pickles import load_pages_from_pickle
    from htw_search.build_index_pickles import (
        compute_paragraph_embeddings_for_bi_encoder,
        dump_paragraph_embeddings_for_bi_encoder,
    )

    # TODO: error handling, etc.
    print("Loading page data...", end="")
    pages = load_pages_from_pickle(get_path_for_pickle_file("pages.pkl"))
    print("done.\nComputing embeddings...", end="", flush=True)
    embeddings = compute_paragraph_embeddings_for_bi_encoder(pages)
    print("done.\nWriting embeddings to file...", end="", flush=True)
    dump_paragraph_embeddings_for_bi_encoder(embeddings)
    print("done.", flush=True)


if __name__ == "__main__":
    app()
