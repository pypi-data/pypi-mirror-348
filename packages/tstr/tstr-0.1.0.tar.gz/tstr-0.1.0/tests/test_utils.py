# type: ignore

import pytest

from tstr import bind, binder, convert, converter, f, normalize, normalize_str, t


def test_converter_repr_conversion():
    assert converter("r")(42) == repr(42)


def test_converter_str_conversion():
    assert converter("s")(42) == str(42)


def test_converter_invalid_conversion():
    with pytest.raises(ValueError):
        converter("invalid")  # type: ignore


def test_convert_no_conversion():
    assert convert(42, None) == 42


def test_convert_with_conversion():
    assert convert(42, "s") == "42"


def test_normalize_str():
    template = t("{42!s:>5}")
    interpolation = template.interpolations[0]
    assert normalize_str(interpolation) == "   42"


def test_normalize_no_conversion():
    template = t("{42}")
    interpolation = template.interpolations[0]
    assert normalize(interpolation) == 42


def test_normalize_with_conversion():
    template = t("{42!s:>5}")
    interpolation = template.interpolations[0]
    assert normalize(interpolation) == "   42"


def test_bind():
    template = t("{42!s}text")
    result = bind(template, normalize_str)
    assert result == "42text"


def test_binder():
    template = t("{42!s}text")
    bound = binder(normalize_str)
    result = bound(template)
    assert result == "42text"


def test_f_with_string():
    assert f("text") == "text"


def test_f_with_template():
    template = t("{42!s}text")
    assert f(template) == "42text"
