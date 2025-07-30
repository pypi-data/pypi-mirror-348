from .parser import PagesSupported, parse_page
from .searchpage import Consoles, Menu, parse_searchpage
from .types import (
    AudioFormat,
    AudioTrack,
    Browsable,
    GameEntry,
    GameListPage,
    GamePage,
    InfoPage,
    ParseError,
)

__all__ = [
    "AudioFormat",
    "AudioTrack",
    "Browsable",
    "Consoles",
    "GameEntry",
    "GameListPage",
    "GamePage",
    "InfoPage",
    "Menu",
    "PagesSupported",
    "parse_page",
    "parse_searchpage",
    "ParseError",
]
