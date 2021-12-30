import dataclasses
from abc import ABC
from dataclasses import dataclass
from typing import Optional

from .formatter import Formatter


@dataclass
class Page:
    url: str = ""
    index: int = -1
    paragraphs: list["Paragraph"] = dataclasses.field(default_factory=list)

    @property
    def paragraph_texts(self):
        return [paragraph.single_line_text for paragraph in self.paragraphs]


@dataclass
class TextOnPage(ABC):
    """
    Text that appears somewhere on a page.

    This class keeps track of the enclosing scope of the text for formatting
    purposes and of the page from which this text originates.
    """

    page: Page
    text: str = ""

    @property
    def single_line_text(self):
        """Return the text with all newlines replaced by spaces."""
        return self.text.replace("\n", " ")

    @property
    def abbreviated_text(self):
        """Return the text truncated to at most 40 chars."""
        return self.text if len(self.text) <= 40 else self.text[:37] + "..."

    def get_emphasized_text(self, output_format="ansi", single_line=False):
        """
        Return the emphasized text for the given output format.

        If single_line is true all newlines in the text are replaced by spaces.
        """
        formatter = Formatter.create(output_format)
        return formatter.emphasize(self.single_line_text if single_line else self.text)

    @property
    def paragraph_text(self):
        """Return the text of the enclosing paragraph."""
        return self.text

    @property
    def single_line_paragraph(self):
        """Return the text of the enclosing paragraph as single line."""
        return self.paragraph_text.replace("\n", " ")

    def get_emphasized_paragraph_text(self, output_format="ansi", single_line=False):
        """
        Return the text of the enclosing paragraph.

        The occurrence of this text in the paragraph is emphasized according to
        the specified output_format.
        """
        formatter = Formatter.create(output_format)
        return formatter.emphasize(
            self.single_line_paragraph if single_line else self.paragraph_text
        )

    @property
    def description(self):
        """Return a short description of this element."""
        return f"{type(self).__name__}({self.page_index})"

    def __str__(self):
        return f"{self.description}: {self.abbreviated_text!r}"


@dataclass
class Paragraph(TextOnPage):
    """A paragraph appearing as content on a page."""

    paragraph_index: int = -1
    sentences: list["Sentence"] = dataclasses.field(default_factory=list)

    @property
    def description(self):
        return f"{type(self).__name__}({self.page.index}, {self.paragraph_index})"


@dataclass
class PageTitle(TextOnPage):
    """The title of the page."""

    pass


@dataclass
class SentenceOnPage(TextOnPage, ABC):
    """A sentence appearing embedded in another element of the page."""


@dataclass
class Sentence(TextOnPage):
    """A sentence appearing as part of a paragraph."""

    paragraph: Optional[Paragraph] = None
    sentence_index: int = -1
    start_char: int = -1
    end_char: int = -1

    def paragraph_text(self):
        return self.paragraph.text

    def get_emphasized_paragraph_text(self, output_format="ansi", single_line=False):
        formatter = Formatter.create(output_format)
        paragraph_text = self.paragraph_text

        return (
            paragraph_text[: self.start_char]
            + formatter.emphasize(self.text)
            + paragraph_text[self.end_char :]
        )

    def description(self):
        return (
            f"Sentence({self.paragraph.paragraph_index!r}, {self.sentence_index!r},"
            f"{self.start_char}:{self.end_char})"
        )
