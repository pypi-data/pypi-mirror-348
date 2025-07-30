# Examples

This page contains practical examples showing how to use the `tstr` package for different use cases.

## Basic Usage

### Converting Templates to Strings

The simplest way to use `tstr` is to convert template strings to regular strings, similar to how f-strings work:

```python
from tstr import f

name = "World"
age = 42
template = t"Hello, {name}! You are {age} years old."
result = f(template)
assert result == "Hello, World! You are 42 years old."
```

### Preserving Types with normalize()

Unlike `normalize_str()`, the `normalize()` function preserves the original type when possible:

```python
from tstr import normalize

# No conversion or format spec - original value preserved
template = t"{42}"
value = normalize(template.interpolations[0])
assert value == 42
assert isinstance(value, int)

# With conversion - returns string
template = t"{42!r}"
value = normalize(template.interpolations[0])
assert value == '42'
assert isinstance(value, str)

# With format spec - returns string
template = t"{42:.2f}"
value = normalize(template.interpolations[0])
assert value == '42.00'
assert isinstance(value, str)
```

## Creating Custom Template Processors

### HTML Escaping for Safe Output

Here's a simple HTML sanitizer using `bind()`:

```python
from tstr import bind, normalize_str

def html_escape(text):
    replacements = {
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#x27;"
    }
    for char, replacement in replacements.items():
        text = text.replace(char, replacement)
    return text

def safe_html(template):
    return bind(template, lambda i: html_escape(normalize_str(i)))

user_input = "<script>alert('XSS')</script>"
template = t"<div>{user_input}</div>"
result = safe_html(template)
assert result == "<div>&lt;script&gt;alert(&#x27;XSS&#x27;)&lt;/script&gt;</div>"
```

### Using binder() to Create Reusable Processors

The `binder()` function can create reusable template processors:

```python
from tstr import binder, normalize_str

# Create a binder that formats numbers specially
@binder
def format_values(interpolation):
    value = interpolation.value
    if isinstance(value, (int, float)):
        return f"[NUM: {value:.2f}]"
    else:
        return normalize_str(interpolation)

# Use the binder with different templates
name = "World"
template1 = t"Count: {42} items"
template2 = t"Price: {19.95} dollars"
template3 = t"Name: {name}"

assert format_values(template1) == "Count: [NUM: 42.00] items"
assert format_values(template2) == "Price: [NUM: 19.95] dollars"
assert format_values(template3) == "Name: World"
```

## Advanced Template Processing

### Custom Joiner Function

The `bind()` and `binder()` functions accept a custom joiner:

```python
from tstr import bind, normalize_str

# Join with newlines instead of concatenating
def process_lines(template):
    return bind(template, normalize_str, joiner="\n".join)

items = ["Apples", "Bananas", "Cherries"]
template = t"Items:{items[0]}{items[1]}{items[2]}"
result = process_lines(template)
assert result == "Items:\nApples\nBananas\nCherries"
```

### Collecting Values into a List

You can return non-string values from binders:

```python
from tstr import bind

def collect_values(template):
    values = []
    
    # Collect interpolation values, ignore strings
    def collector(interp):
        values.append(interp.value)
        return ""
    
    # The result is discarded, we just want the side-effect
    bind(template, collector)
    
    return values

name = "World"
age = 42
template = t"Name: {name}, Age: {age}"
values = collect_values(template)
assert values == ["World", 42]
```

### Safe SQL Query Building

Create a safe SQL query builder that prevents SQL injection:

```python
from tstr import bind

def sql_safe(template):
    params = []
    
    def process_param(interp):
        params.append(interp.value)
        return "?"  # Use placeholders
    
    query = bind(template, process_param)
    
    return query, params

user_id = "user123'; DROP TABLE users; --"
template = t"SELECT * FROM users WHERE id = {user_id}"
query, params = sql_safe(template)

assert query == "SELECT * FROM users WHERE id = ?"
assert params == ["user123'; DROP TABLE users; --"]

# Usage with a DB API:
# cursor.execute(query, params)
```

### Context-Aware Processing

This example shows how to process interpolations differently based on context:

```python
from tstr import bind, normalize_str
import re

def smart_template(template):
    # Track whether we're inside an attribute value
    in_attr = False
    attr_name = None
    
    def process(item):
        nonlocal in_attr, attr_name
        
        if isinstance(item, str):
            # Check for attribute context
            attr_match = re.search(r'(\w+)="$', item)
            if attr_match:
                in_attr = True
                attr_name = attr_match.group(1)
            elif in_attr and item.startswith('"'):
                in_attr = False
                attr_name = None
            return item
        else:
            # Process interpolation based on context
            value = item.value
            
            if in_attr and attr_name == "data-json":
                # JSON-encode values in data-json attributes
                import json
                return json.dumps(value)
            elif isinstance(value, dict) and not attr_name:
                # Convert dict to HTML attributes
                return " ".join(f'{k}="{v}"' for k, v in value.items())
            else:
                # Default processing
                return normalize_str(item)
    
    return bind(template, process)

# Usage
attrs = {"id": "user-profile", "class": "card"}
data = {"name": "John", "age": 30}
template = t'<div {attrs} data-json="{data}">User info</div>'

result = smart_template(template)
assert result == '<div id="user-profile" class="card" data-json="{"name": "John", "age": 30}">User info</div>'
```
