from typing import Iterable

import joblib
import torch
from toolz import concat

from .page import Page, Paragraph
from .utils.env import load_config
from .utils.paths import get_path_for_pickle_file

from .utils.transformers import bi_encoder

_config = load_config()


top_k = _config["top_k"]
batch_size = _config["batch_size"]


def compute_paragraph_embeddings_for_bi_encoder(pages: Iterable[Page]):
    paragraphs = list(concat(page.paragraphs for page in pages))
    texts = [paragraph.single_line_text for paragraph in paragraphs]
    paragraph_embeddings = bi_encoder.encode(
        texts, convert_to_tensor=True, show_progress_bar=True, batch_size=batch_size
    )
    paragraph_embeddings = paragraph_embeddings.cpu()
    return paragraph_embeddings, paragraphs


def dump_paragraph_embeddings_for_bi_encoder(embeddings_and_paragraphs):
    joblib.dump(
        embeddings_and_paragraphs,
        get_path_for_pickle_file("bi_encoder_paragraph_embeddings.pkl"),
    )


def load_paragraph_embeddings_for_bi_encoder() -> tuple[
    list[torch.Tensor], list[Paragraph]
]:
    return joblib.load(get_path_for_pickle_file("bi_encoder_paragraph_embeddings.pkl"))
