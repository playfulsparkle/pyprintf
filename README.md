# pyprintf

A Python implementation of the C-style sprintf() function.

## Installation

```bash
pip install pyprintf
```

## Usage

```python
from pyprintf import sprintf

# Basic formatting
output = sprintf("Hello, %s!", "world")
print(output)  # Output: Hello, world!

# Multiple arguments
output = sprintf("%s has %d apples", "John", 5)
print(output)  # Output: John has 5 apples

# Float formatting
output = sprintf("Pi is approximately %.2f", 3.14159)
print(output)  # Output: Pi is approximately 3.14
```