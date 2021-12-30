# %%
from abc import ABC
from typing import ClassVar
from dataclasses import dataclass

from colorama import Fore


# %%
@dataclass
class Formatter(ABC):
    @staticmethod
    def create(output_format: str = "noop"):
        if output_format.lower() == "ansi":
            return AnsiFormatter()
        elif output_format.lower() == "html":
            return HtmlFormatter()
        else:
            return NoopFormatter()

    @classmethod
    def emphasize(cls, text):
        return text

    @classmethod
    def strong(cls, text):
        return text


# %%
@dataclass
class NoopFormatter(Formatter):
    pass


# %%
@dataclass
class AnsiFormatter(Formatter):
    # These definitions may work better with bright backgrounds
    # start_tag: ClassVar[str] = Fore.GREEN + Back.BLACK
    # strong_start_tag: ClassVar[str] = Fore.RED + Back.BLACK
    # end_tag: ClassVar[str] = Back.RESET + Fore.RESET
    emph_start_tag: ClassVar[str] = Fore.GREEN
    strong_start_tag: ClassVar[str] = Fore.RED
    end_tag: ClassVar[str] = Fore.RESET

    @classmethod
    def emphasize(cls, text):
        return cls.emph_start_tag + text + cls.end_tag

    @classmethod
    def strong(cls, text):
        return cls.strong_start_tag + text + cls.end_tag


# %%
@dataclass
class HtmlFormatter(Formatter):
    emph_start_tag: ClassVar[str] = r'<span class="emph">'
    strong_start_tag: ClassVar[str] = r'<span class="emph strong">'
    end_tag: ClassVar[str] = r"</span>"

    @classmethod
    def emphasize(cls, text):
        return cls.emph_start_tag + text + cls.end_tag

    @classmethod
    def strong(cls, text):
        return cls.strong_start_tag + text + cls.end_tag


# %%
