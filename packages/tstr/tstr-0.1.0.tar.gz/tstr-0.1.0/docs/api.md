# tstr API Documentation

This document provides detailed explanations of the `tstr` API for processing template strings.

# API Reference

## Core Functions

### `f(template)`

```python
def f(template: Template) -> str:
```

Renders a template as a string, just like f-strings.

**Parameters:**
- `template (Template)`: The template to render.

**Returns:**
- `str`: The rendered string.

**Example:**
```python
name = "world"
template = t"Hello, {name}!"
result = f(template)
assert result == "Hello, world!"
```

### `evaluate(template)`

Alias for `f()`.

### `normalize(interpolation)`

```python
def normalize(interpolation: Interpolation) -> str | object:
```

Normalizes a PEP 750 Interpolation, preserving its type when possible.

If neither a conversion nor a format spec is specified, the original value
is returned without any modification, ensuring that the value's type is preserved.

**Parameters:**
- `interpolation (Interpolation)`: The interpolation to normalize.

**Returns:**
- `str | object`: The normalized string if conversion or format spec is specified, otherwise the original value.

**Example:**
```python
template = t"{42}"
interpolation = template.interpolations[0]
value = normalize(interpolation)
assert value == 42
assert isinstance(value, int)
```

### `normalize_str(interpolation)`

```python
def normalize_str(interpolation: Interpolation) -> str:
```

Normalizes a PEP 750 Interpolation to a formatted string.

This processes an Interpolation object similarly to how f-strings process
interpolated expressions: it applies any conversion and format specification.
Unlike normalize(), this always returns a string.

**Parameters:**
- `interpolation (Interpolation)`: The interpolation to normalize.

**Returns:**
- `str`: The formatted string representation of the interpolation.

**Example:**
```python
template = t"{42!s:>5}"
interpolation = template.interpolations[0]
result = normalize_str(interpolation)
assert result == "   42"
```

## Template Processing

### `bind(template, binder, *, joiner="".join)`

```python
def bind(
    template: Template,
    binder: Callable[[Interpolation], T],
    *,
    joiner: Callable[[Iterable[T | str]], U] = "".join,
) -> U:
```

Binds a template by processing its interpolations using a binder function
and combining the results with a joiner function.

This function processes each `Interpolation` in the given template using the
provided `binder` function, and then combines the processed parts using the
`joiner` function. By default, the `joiner` concatenates the parts into a single
string.

**Parameters:**
- `template (Template)`: A template to process.
- `binder (Callable)`: A callable that transforms each Interpolation.
- `joiner (Callable)`: A callable to join the processed template parts. Defaults to "".join.

**Returns:**
- `Any`: The result of the joiner function applied to the processed parts.

**Example:**
```python
def uppercase_values(interp):
    return str(interp.value).upper()

name = "world"    
template = t"Hello {name}!"
result = bind(template, uppercase_values)
assert result == "Hello WORLD!"
```

### `binder(binder, joiner="".join)`

```python
def binder(
    binder: Callable[[Interpolation], T],
    joiner: Callable[[Iterable[T | str]], U] = "".join,
) -> Callable[[Template], U]:
```

Creates a reusable template processor function from a binder function.

This is a higher-order function that creates specialized template processors.
Use this when you want to process multiple templates with the same transformation.

Additionally, this can be used as a decorator to create reusable template
processors in a concise and readable way.

**Parameters:**
- `binder (Callable)`: A function that transforms Interpolation objects.
- `joiner (Callable)`: A function to join the processed template parts. Defaults to "".join.

**Returns:**
- `Callable[[Template], Any]`: A function that processes templates using the given binder.

**Example:**
```python
from html import escape

@binder
def html_safe(interpolation: Interpolation) -> str:
    # Example binder that escapes HTML in interpolations
    return escape(normalize_str(interpolation))

username = "<script>alert('XSS')</script>"
template = t"Hello, {username}!"
result = html_safe(template)
assert result == "Hello, &lt;script&gt;alert(&#x27;XSS&#x27;)&lt;/script&gt;!"
```

## Conversion Functions

### `converter(conversion)`

```python
def converter[T](conversion: Conversion) -> Callable[[T], T | str]:
```

Returns a callable that converts a value based on PEP 750 conversion specifiers.

This function is the backbone of handling conversions like those in f-strings and
template strings (e.g., !r, !s, !a). It maps conversion specifiers to their
corresponding conversion functions: "a" returns `ascii`, "r" returns `repr`,
and "s" returns `str`.

**Parameters:**
- `conversion (Conversion)`: The conversion specifier.

**Returns:**
- `Callable[[T], T | str]`: A function that performs the specified conversion.

**Raises:**
- `ValueError`: If the conversion specifier is not one of the allowed values.

**Example:**
```python
repr_func = converter("r")
result = repr_func(42)
assert result == "42"
```

### `convert(value, conversion)`

```python
def convert[T](value: T, conversion: Conversion | None) -> T | str:
```

Applies a PEP 750 conversion to a value.

While template strings preserve the conversion specification in the Interpolation
object, this function actually applies that conversion to produce the final value,
similar to how f-strings process conversions.

**Parameters:**
- `value (T)`: The value to convert, typically from an Interpolation.value.
- `conversion (Conversion | None)`: The conversion specifier (!r, !s, !a), or None.

**Returns:**
- `T | str`: The converted value, or the original if no conversion is specified.

**Example:**
```python
result1 = convert(42, "s")
assert result1 == "42"

result2 = convert(42, None)
assert result2 == 42
assert isinstance(result2, int)
```

## Utility Functions

### `template_eq(template1, template2, /, *, compare_value=True, compare_expr=True)`

```python
def template_eq(
    template1: Template, 
    template2: Template, 
    /, 
    *, 
    compare_value: bool = True, 
    compare_expr: bool = True
) -> bool:
```

Compares two Template objects for equivalence.

This function checks whether two Template instances are equivalent by comparing their string and interpolation parts.

**Parameters:**
- `template1 (Template)`: The first template to compare.
- `template2 (Template)`: The second template to compare.
- `compare_value (bool, optional)`: If False, the 'value' attribute of each interpolation is not compared. Defaults to True.
- `compare_expr (bool, optional)`: If False, the 'expression' attribute of each interpolation is not compared. Defaults to True.

**Returns:**
- `bool`: True if the templates are considered equivalent based on the specified criteria, False otherwise.

**Example:**
```python
name = "World"
template1 = t"Hello {name}"
template2 = t"Hello {name}"
assert template_eq(template1, template2) is True

# Compare structure only, not values
name = "Different"
template3 = t"Hello {name}"
assert template_eq(template1, template3, compare_value=False) is True
assert template_eq(template1, template3, compare_value=True) is False
```
