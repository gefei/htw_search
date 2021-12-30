from htw_search.formatter import Formatter, AnsiFormatter, HtmlFormatter, NoopFormatter


# %%
def test_create_noop_formatter():
    formatter = Formatter.create()
    assert type(formatter) == NoopFormatter


# %%
def test_noop_formatter_emphasize():
    formatter = Formatter.create()
    assert formatter.emphasize("abc") == "abc"


# %%
def test_noop_formatter_strong():
    formatter = Formatter.create()
    assert formatter.emphasize("abc") == "abc"


# %%
def test_create_ansi_formatter():
    formatter = Formatter.create("ansi")
    assert type(formatter) == AnsiFormatter


# %%
def test_ansi_formatter_emphasize():
    formatter = Formatter.create("ansi")
    assert "foo and bar" in formatter.emphasize("foo and bar")
    assert len(formatter.emphasize("abc")) > 3


# %%
def test_ansi_formatter_strong():
    formatter = Formatter.create("ansi")
    assert "foo and bar" in formatter.strong("foo and bar")
    assert len(formatter.strong("abc")) > 3


# %%
def test_create_html_formatter():
    formatter = Formatter.create("html")
    assert type(formatter) == HtmlFormatter


# %%
def test_html_formatter_emphasize():
    formatter = Formatter.create("html")
    assert formatter.emphasize("abc") == '<span class="emph">abc</span>'


# %%
def test_html_formatter_strong():
    formatter = Formatter.create("html")
    assert formatter.strong("abc") == '<span class="emph strong">abc</span>'
