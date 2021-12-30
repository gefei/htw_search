from htw_search.build_page_pickles import (
    parse_text_into_paragraphs_and_sentences,
    build_single_page,
    build_pages,
)
from htw_search.page import Page, Paragraph, Sentence


def test_parsing_empty_page():
    page = Page()
    result = parse_text_into_paragraphs_and_sentences(page, "")
    assert result == []


def test_parsing_page_with_one_paragraph():
    page = Page()
    paragraph_text = "This, is some   text."
    result_text = paragraph_text  # Maybe change this to remove whitespace...
    result = parse_text_into_paragraphs_and_sentences(page, paragraph_text)
    paragraph = result[0]
    assert result == [
        Paragraph(
            page=page,
            text=result_text,
            paragraph_index=0,
            sentences=[
                Sentence(
                    page=page,
                    paragraph=paragraph,
                    text=result_text,
                    sentence_index=0,
                    start_char=0,
                    end_char=len(paragraph_text),
                )
            ],
        )
    ]


_paragraphs = (
    "This is some text!! It seems.\n\n\n\nSplit into three paragraphs?!?!?!\n\n"
    "With some additional line ends...\n\n\n"
)


def test_parsing_page_with_multiple_paragraphs():
    page = Page()
    result = parse_text_into_paragraphs_and_sentences(page, _paragraphs)
    assert len(result) == 3
    assert result[0].text == "This is some text!! It seems."
    assert len(result[0].sentences) == 2
    assert result[0].sentences[0].text == "This is some text!!"
    assert result[1].text == "Split into three paragraphs?!?!?!"
    assert result[2].text == "With some additional line ends..."


def test_build_single_page():
    page = build_single_page(
        {"url": "http://example.com/", "text": "The text of the page.\n\nIs here."},
        page_index=7,
    )
    assert isinstance(page, Page)
    assert len(page.paragraphs) == 2
    assert page.url == "http://example.com/"
    assert page.paragraphs[0].text == "The text of the page."
    assert page.index == 7


def test_build_pages():
    page_descrs = [
        {"url": "foo.com", "text": "FOO"},
        {"url": "bar.org", "text": "BAR\n\nBAZ"},
    ]
    pages = build_pages(page_descrs)
    assert len(pages) == 2
    assert pages[0].index == 0
    assert len(pages[0].paragraphs) == 1
    assert pages[0].paragraphs[0].text == "FOO"
    assert pages[1].index == 1
    assert len(pages[1].paragraphs) == 2
    assert pages[1].paragraphs[0].text == "BAR"
    assert pages[1].paragraphs[1].text == "BAZ"
