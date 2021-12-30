import json
import pickle
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from syntok import segmenter
from toolz import concat

from .page import Paragraph, Sentence, Page
from .utils import env

_config = env.load_config()

num_processes = _config["num_processes"]
max_paragraphs_per_page = _config["max_paragraphs_per_page"]
max_sentences_per_paragraph = _config["max_sentences_per_paragraph"]


def parse_text_into_paragraphs_and_sentences(page: Page, text: str):
    paragraphs = []
    for paragraph_index, paragraph_segments in enumerate(segmenter.process(text)):
        paragraph = Paragraph(page=page, paragraph_index=paragraph_index)
        sentences = [
            Sentence(
                page=page,
                paragraph=paragraph,
                text=str.lstrip("".join([tok.spacing + tok.value for tok in sentence])),
                sentence_index=sentence_index,
                start_char=sentence[0].offset,
                end_char=sentence[-1].offset + 1,
            )
            for sentence_index, sentence in enumerate(paragraph_segments)
        ]
        paragraph.sentences = sentences
        paragraph.text = " ".join(s.single_line_text for s in sentences)
        if len(paragraph.text) > 0:
            paragraphs.append(paragraph)
    return paragraphs


def build_single_page(page_descr: dict, page_index: int):
    page = Page(url=page_descr["url"], index=page_index)
    text = page_descr["text"]
    paragraphs = parse_text_into_paragraphs_and_sentences(page, text)
    page.paragraphs = paragraphs
    return page


def build_pages(page_descrs: Iterable[dict]):
    return [
        build_single_page(page_descr, page_index)
        for page_index, page_descr in enumerate(page_descrs)
    ]


def parse_jsonl_file_from_crawl(path: Path):
    with open(path, "r", encoding="utf-8") as file:
        lines = file.readlines()
    page_descrs = (json.loads(line) for line in lines)
    return build_pages(page_descrs)


def save_pages_as_pickle(pages: Iterable[Page], path: Path):
    with open(path, "wb") as file:
        pickle.dump(pages, file)


def load_pages_from_pickle(path: Path):
    with open(path, "rb") as file:
        return pickle.load(file)
