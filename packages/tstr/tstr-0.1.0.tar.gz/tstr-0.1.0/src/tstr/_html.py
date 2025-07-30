from html import escape

from tstr import Interpolation, binder

__all__ = ["html_safe"]


@binder
def html_safe(interpolation: Interpolation) -> str:
    """
    Escapes HTML special characters in interpolations for safe HTML rendering.

    This function helps prevent XSS attacks by escaping any HTML special
    characters in interpolated values. It's specifically designed for safely
    including user-provided content in HTML templates.

    Special behavior:
        - When the 'r' conversion is used (e.g., {content!r}), the value is treated as
          raw HTML and will NOT be escaped. This allows for intentional inclusion of
          HTML markup when needed.
        - Other conversion specifiers ('s', 'a') are not allowed to avoid confusion.

    Args:
        template (Template): The template to process.

    Returns:
        str: The HTML-escaped string, or unescaped if using the 'r' conversion.

    Raises:
        ValueError: If any conversion specifier other than 'r' is used.

    Example:
        ```python
        from tstr._html import html_safe

        # Unsafe user input that will be safely escaped
        username = "<script>alert('XSS')</script>"
        template = t"<div>Welcome, {username}!</div>"
        result = html_safe(template)
        assert result == "<div>Welcome, &lt;script&gt;alert(&#x27;XSS&#x27;)&lt;/script&gt;!</div>"

        # Intentionally including raw HTML with the 'r' conversion
        title_html = "<b>Important Notice</b>"
        template = t"<h1>{title_html!r}</h1>"
        result = html_safe(template)
        assert result == "<h1><b>Important Notice</b></h1>"
        ```
    """
    formatted = format(interpolation.value, interpolation.format_spec)
    if interpolation.conversion == "r":
        return formatted
    elif interpolation.conversion:
        raise ValueError("Conversion other than 'r' is prohibited.")
    else:
        return escape(formatted)
