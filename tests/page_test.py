from htw_search.page import Page, TextOnPage


class TextStub(TextOnPage):
    pass


def test_single_line_text():
    text_stub = TextStub(Page(), "a\nb\nc")
    assert text_stub.single_line_text == "a b c"


def test_abbreviated_text_for_short_text():
    short_text = "1234567890" * 4
    text_stub = TextStub(Page(), short_text)
    assert text_stub.abbreviated_text == short_text


def test_abbreviated_text_for_long_text():
    prefix = "1234567890" * 3 + "1234567"
    long_text = prefix + "8901"
    text_stub = TextStub(Page(), long_text)
    assert text_stub.abbreviated_text == prefix + "..."


def test_get_emphasized_text():
    text = "a\nb\nc"
    text_stub = TextStub(Page(), text)
    assert (
        text_stub.get_emphasized_text("html", single_line=False)
        == '<span class="emph">' + text + "</span>"
    )


def test_get_emphasized_text_single_line():
    text = "a\nb\nc"
    text_stub = TextStub(Page(), text)
    assert (
        text_stub.get_emphasized_text("html", single_line=True)
        == '<span class="emph">a b c</span>'
    )
