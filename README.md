# pyprintf: Lightweight Python String Formatting Library

[![PyPI Version](https://img.shields.io/pypi/v/pyprintf.svg)](https://pypi.org/project/pyprintf/)
[![Python Versions](https://img.shields.io/pypi/pyversions/pyprintf.svg)](https://pypi.org/project/pyprintf/)
[![License](https://img.shields.io/badge/License-BSD_3--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)

A **lightweight** and **open-source Python package** providing a robust **sprintf implementation** for **type-safe string formatting**. This library offers a familiar syntax for developers accustomed to `sprintf` from C and PHP, with enhanced Pythonic features including:

- **Positional & Named Placeholders**
- **Cross-version Compatibility** (Python 3.11+)
- **Strict Type Validation**
- **JSON Serialization Support**
- **Configurable Formatting Rules**

## Usage

Here's a quick example to get you started:

```python
from pyprintf import sprintf

name = "World"
count = 42

# Simple positional formatting
greeting = sprintf("Hello %s!", name)
print(greeting)  # Output: Hello World!

# Formatting with a number
message = sprintf("The answer is %d.", count)
print(message)  # Output: The answer is 42.
```

## Installation

### PyPi

```bash
pip install pyprintf
```

## API

### `sprintf`

The primary formatting function that mimics C-style `sprintf` behavior with Python enhancements.

**Parameters:**
- `format` (str): Format string containing text and placeholders
- `*args` (Any): Variable arguments to format (positional or keyword)

**Returns:**
- `str`: Formatted string according to specifiers

**Signature:**
```python
def sprintf(format: str, *args: Any) -> str:
```

**Example:**
```python
from pyprintf import sprintf

# Positional arguments
output = sprintf("%s has %d apples", "Alice", 5)
# "Alice has 5 apples"

# Named arguments
output = sprintf("Hello %(name)s!", {"name": "Bob"})
# "Hello Bob!"
```

### `vsprintf`

Array-accepting variant of `sprintf` for pre-collected arguments.

***Parameters:***

- `format` (str): Format string containing text and placeholders
- `*args` (Any): Variable arguments to format (positional or keyword)

***Return Value:***

- `str`: Formatted string according to specifiers

**Signature:**
```python
def vsprintf(format: str, *args: Any) -> str:
```

### Difference between `sprintf` and `vsprintf`

The main difference is how they receive the values to be formatted: `sprintf` takes them as individual arguments after the format string, while `vsprintf` takes them as a single iterable (like a list or tuple) argument. `vsprintf` is useful when the arguments are already collected in a data structure.

## Format String Placeholders

The `sprintf` function uses placeholders within the format string (the first argument) to indicate where and how subsequent arguments should be inserted and formatted. Placeholders begin with a `%` character and are followed by a sequence of optional formatting options and a required type specifier. This powerful system allows for precise control over the output format of your strings.

### Optional Formatting Elements

These elements can appear in a placeholder in a specific order between the `%` and the type specifier.

1.  **Argument Index (Positional Specifier)**:
    * **Syntax:** A number (starting from 1) followed by a `$` (e.g., `%2$s`).
    * **Description:** Explicitly selects which argument to use for the current placeholder. If omitted, arguments are used sequentially in the order they are provided to `sprintf`.
    * **Example:** `sprintf("%2$s, %1$s!", "Hello", "World")` will output `"World, Hello!"`.

2.  **Sign Indicator**:
    * **Syntax:** A `+` character (e.g., `%+d`).
    * **Description:** Forces numeric values (integers and floats) to always display a sign, either `+` for positive numbers or `-` for negative numbers. By default, only negative numbers show a sign.
    * **Example:** `sprintf("%+d", 5)` will output `"+5"`, and `sprintf("%+d", -5)` will output `"-5"`.

3.  **Padding Specifier**:
    * **Syntax:** Either a `0` or a single quote `'` followed by any character (e.g., `%05d`, `%'*5s`).
    * **Description:** Specifies the character used for padding the output to reach the desired width.
        * Using `0` pads with leading zeros for numeric types.
        * Using `'` followed by a character pads with that specific character.
    * **Examples:**
        * `sprintf("%05d", 12)` will output `"00012"`.
        * `sprintf("%'*5s", "abc")` will output `"**abc"`.

4.  **Alignment**:
    * **Syntax:** A `-` character (e.g., `%-10s`).
    * **Description:** Aligns the output to the left within the specified field width. If the `-` is omitted, the output is right-aligned by default.
    * **Example:** `sprintf("%-10s", "hello")` will output `"hello     "`, and `sprintf("%10s", "hello")` will output `"     hello"`.

5.  **Width**:
    * **Syntax:** A positive integer (e.g., `%10s`, `%5j`).
    * **Description:** Specifies the minimum number of characters to output. If the value to be formatted is shorter than the width, it will be padded (using the padding character and alignment). For the `j` (JSON) type, this number defines the indentation level (number of spaces).
    * **Examples:**
        * `sprintf("%10s", "test")` will output `"      test"`.
        * `sprintf("%5j", { a: 1 })` will output `"{\n     "a": 1\n}"`.

6.  **Precision**:
    * **Syntax:** A period `.` followed by a non-negative integer (e.g., `%.2f`, `%.5g`, `%.10s`).
    * **Description:** Controls the precision of the output depending on the type specifier:
        * For floating-point types (`e`, `f`): Specifies the number of digits to appear after the decimal point.
        * For the `g` type: Specifies the number of significant digits.
        * For the `s`, `t`, `T`, and `v` types: Specifies the maximum number of characters to output (truncates the string if it's longer).
    * **Examples:**
        * `sprintf("%.2f", 3.14159)` will output `"3.14"`.
        * `sprintf("%.5g", 123.45678)` will output `"123.46"`.
        * `sprintf("%.5s", "This is a long string")` will output `"This "`.

### Required Type Specifier

This single character at the end of the placeholder determines how the corresponding argument will be interpreted and formatted.

| Specifier | Description                                                  | Python Example                            | Output               |
| --------- | ------------------------------------------------------------ | ----------------------------------------- | -------------------- |
| `%%`      | Outputs a literal percent sign                               | `sprintf("%%")`                           | `%`                  |
| `b`       | Integer in binary format                                     | `sprintf("%b", 10)`                       | `1010`               |
| `c`       | Integer as Unicode character                                 | `sprintf("%c", 65)`                       | `A`                  |
| `d`/`i`   | Signed decimal integer                                       | `sprintf("%d", 123)`                      | `123`                |
| `e`       | Floating point in scientific notation (lowercase "e")        | `sprintf("%e", 123.45)`                   | `1.234500e+02`       |
| `E`       | Floating point in scientific notation (uppercase "E")        | `sprintf("%E", 123.45)`                   | `1.234500E+02`       |
| `f`       | Floating point with decimal precision                        | `sprintf("%.2f", 3.14159)`                | `3.14`               |
| `g`       | Adaptive float formatting                                    | `sprintf("%.3g", 1234.56)`                | `1.23e+03`           |
| `o`       | Integer in octal format                                      | `sprintf("%o", 10)`                       | `12`                 |
| `s`       | String output                                                | `sprintf("%s", "hello")`                  | `hello`              |
| `t`       | Boolean (`"True"`/`"False"` capitalized strings)             | `sprintf("%t", True)`                     | `True`               |
| `T`       | Python type name (`"list"`/`"NoneType"` capitalized strings) | `sprintf("%T", [])`                       | `list`               |
| `u`       | Unsigned decimal integer (32-bit wrap)                       | `sprintf("%u", -5)`                       | `4294967291`         |
| `x`       | Integer in lowercase hexadecimal                             | `sprintf("%x", 255)`                      | `ff`                 |
| `X`       | Integer in uppercase hexadecimal                             | `sprintf("%X", 255)`                      | `FF`                 |
| `j`       | Python object in JSON format                                 | `sprintf("%j", {"a": 1})`                 | `{"a": 1}`           |

## Features

### Flexible Configuration Options

Our `sprintf` library offers powerful and flexible configuration options to tailor its behavior to your specific needs. You can easily adjust settings like how unmatched placeholders are handled or whether computed values are allowed. This section outlines the various ways you can configure the library.

#### Chainable Configuration

For more control, you can leverage our chainable configuration interface. This allows you to set multiple configuration options in a fluent and readable manner.

**Method 1: Chaining Method Calls**

You can chain configuration methods directly before calling `sprintf()`:

```python
from pyprintf import config

result = config() \
    .allow_computed_value(True) \
    .preserve_unmatched_placeholder(True) \
    .sprintf("My name is %s and I have %d %s. Today is %s", "John", 5, lambda: "apple")
print(result)  # Output: My name is John and I have 5 apple. Today is %s
```

**Method 2: Using a Configuration Object**

Alternatively, you can pass a JavaScript object containing your desired configuration options to the `config()` method:

```python
sprintf_config = config(
    allow_computed_value=True,
    preserve_unmatched_placeholder=True
).sprintf("My name is %s and I have %d %s. Today is %s", "John", 5, lambda: "apple")
print(sprintf_config)  # Output: My name is John and I have 5 apple. Today is %s
```

#### Reusing Configurations

One of the key benefits of our configuration system is the ability to create reusable configuration objects. This is particularly useful when you have consistent formatting requirements across different parts of your application.

```python
sprintf_config = config().allow_computed_value(True)

result1 = sprintf_config.sprintf("%s", lambda: "test1")
print(result1)  # Output: test1

result2 = sprintf_config.sprintf("%s", lambda: "test2") 
print(result2)  # Output: test2
```

In this example, `sprintfConfig` retains the `allowComputedValue(true)` setting, allowing you to apply it to multiple `sprintf()` calls without repeating the configuration.

#### Analyzing placeholder statistic with getStats()

A new `getStats()` method, accessible through the chainable configuration, allows you to analyze the placeholders in your format strings.

```python
cfg = config()
cfg.sprintf("%s %s %s %s %(name)s %1$s %2$s")
print(cfg.get_stats())
# Output: {
#   "total_placeholders": 7,
#   "total_named_placeholder": 1,
#   "total_positional_placeholder": 2,
#   "total_sequential_positional_placeholder": 4
# }
```

### Flexible Argument Order

You can specify the order of values in the formatted string independently from how they are provided. By adding a number (like `%1$s`, `%2$s`) to the placeholder, you control which value is used and in which position. This also allows reusing the same value multiple times without passing it again. This feature enhances the flexibility and readability of your code.

__Example:__

```python
sprintf("%2$s is %1$s years old and loves %3$s", 25, "John", "basketball")
// Returns: "John is 25 years old and loves basketball"
```

Here, `%2$s` refers to the second argument (`John`), `%3$s` to the third (`basketball`), and `%1$s` to the first (`25`).

### Named Placeholders

Instead of using numbers, you can reference values by their names using objects. Placeholders are wrapped in parentheses, like `%(keyword)s`, where `keyword` matches a key in the provided object. This makes the code more readable and works with nested data, improving the maintainability of your string formatting logic.

* Basic usage:

__Example:__

```python
user_obj = {"name": "John"}
print(sprintf("Hello %(name)s", user_obj))  # Output: Hello John
```

* Nested data (dictionaries/lists):

__Example:__

```python
data = {
    "users": [
        {"name": "Jane"},
        {"name": "Jack"}
    ]
}
print(sprintf("Hello %s, %(users[0].name)s, and %(users[1].name)s", "John", data))
# Output: Hello John, Jane, and Jack
```

### Named and positional placeholder

`sprintf` offers exceptional flexibility by allowing you to utilize **named placeholders** (like `%(keyword)s`), **numbered positional placeholders** (such as `%1$s`, `%2$s`), and **sequential positional placeholders** (represented by `%s`). This comprehensive support enables you to choose the most appropriate style, or even combine them for complex formatting scenarios, enhancing both readability and maintainability.

* Basic usage:

__Example:__

```python
data = {"name": "Polly"}
print(sprintf("%(name)s %2$s a %1$s", "cracker", "wants", data))
# Output: Polly wants a cracker
```

### Leveraging `preserveUnmatchedPlaceholder` functionality

You can use the `preserveUnmatchedPlaceholder` option to perform multi-stage string formatting with `sprintf`. This allows you to initially apply a subset of data, leaving unmatched placeholders in place to be filled in later.

```python
cfg = config(preserve_unmatched_placeholder=True)
first_pass = cfg.sprintf("My name is %(firstname)s %(lastname)s", {"lastname": "Doe"})
print(first_pass)  # Output: My name is %(firstname)s Doe

print(cfg.sprintf(first_pass, {"firstname": "John"}))  # Output: My name is John Doe
```

### Computed values

To generate values dynamically, you can supply a function. This function will be invoked without arguments, and its return value will be treated as the computed value.

We have exposed the `allowComputedValue` property, which allows you to enable or disable this functionality. If you intend to use `sprintf` with function arguments for dynamic values, you must explicitly enable this feature by setting `sprintf.allowComputedValue = true`. This functionality is disabled by default due to potential security concerns.

**Security Consideration:**

Enabling computed values introduces a risk if the format string or the arguments passed to `sprintf` come from an untrusted source. For example, a malicious actor could potentially inject a format string with a placeholder that triggers the execution of a function they also control.

**Example of Potential Risk:**

While this is a simplified illustration, imagine a scenario where user input could influence the arguments passed to `sprintf`:

```python
from pyprintf import config

# WARNING: Enabling computed values with untrusted input is risky!
cfg = config().allow_computed_value(True)

user_input = "%s"  # Could be controlled by a malicious user

malicious_function = lambda: (
    # In a real attack, this could execute harmful code
    print("Malicious function executed!") or 
    "dangerous output"
)

formatted = cfg.sprintf(user_input, malicious_function)
print(formatted)  # Output: "dangerous_output"
# Console shows: "Malicious function executed!"
```

In this example, if `userInput` was crafted to include `%s` and a malicious function was somehow passed as an argument, enabling `allowComputedValue` would lead to the execution of that function.

**Example (Safe Usage):**

When using computed values with trusted input:

```python
from datetime import datetime

cfg = config().allow_computed_value(True)

result = cfg.sprintf(
    "Current date and time: %s",
    lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S")
)
print(result)  # Output: "Current date and time: 2025-04-10 13:25:07"
```

Remember to enable `config().allow_computed_value(True)` only when you are certain about the safety and origin of the format string and its arguments.

## License

**pyprintf** is licensed under the terms of the BSD 3-Clause License.
