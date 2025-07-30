from htmlmin import minify
from html import escape as html_escape, unescape as html_unescape

from xspider.types import Any


def compress(html: str, /, **kwargs: Any) -> str:
    return minify(html, **kwargs)


def escape(text: str) -> str:
    """
    >>> escape("<")
    '&lt;'

    """
    return html_escape(text)


def unescape(text: str) -> str:
    """
    >>> unescape("&lt;")
    '<'

    """
    return html_unescape(text)
