# type: ignore

import pytest
from tstr._html import html_safe
from tstr import t


def test_html_safe_escapes_html():
    username = "<script>alert('XSS')</script>"
    template = t("Hello, {username}!")
    result = html_safe(template)
    assert result == "Hello, &lt;script&gt;alert(&#x27;XSS&#x27;)&lt;/script&gt;!"


def test_html_safe_allows_raw_html():
    raw_html = "<b>BOLD TITLE</b>"
    template = t("<h1>{raw_html!r}</h1>")
    result = html_safe(template)
    assert result == "<h1><b>BOLD TITLE</b></h1>"


def test_html_safe_raises_on_invalid_conversion():
    val = 42
    template = t("{val!s}")
    with pytest.raises(ValueError):
        html_safe(template)


def test_html_safe_with_format_spec():
    val = "hello"
    template = t("{val: >10}")
    result = html_safe(template)
    assert result == "     hello"
