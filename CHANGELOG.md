# Change Log

All notable changes to the pyprintf project will be documented in this file.

## [0.0.8] - 2025-04-18

**Character Handling (`%c`):**  
* Added modulo 256 truncation to align with C's `unsigned char` behavior, ensuring values wrap within 0-255.  
* Negative inputs now wrap via modulo 256 (e.g., `-1` becomes `255`).  

**Binary Handling (`%b`):**  
* Negative numbers now use 32-bit two's complement (e.g., `-5` becomes `11111111111111111111111111111011`).  
* Values are truncated to 32 bits via `& 0xFFFFFFFF` to mimic C's integer overflow.  

## [0.0.7] - 2025-04-18

* Normalized scientific notation format (`e`, `E`) to align with C++ conventions.

## [0.0.6] - 2025-04-18

* Resolved an issue where the `E` (exponential) format specifier was not recognized by the parser.

## [0.0.5] - 2025-04-17

* Added support for uppercase `E` in scientific notation output for floating-point numbers through the `%E` format specifier (e.g., `1.234500E+02`), alongside the existing lowercase `e` format (`%e`).
* Updated documentation to clarify that Python booleans are displayed as capitalized strings (`True`/`False`) when converted to strings.
* Improved type name handling to properly respect Python's standard type name capitalization (e.g., `list`, `dict`, `NoneType`) when using `T` format (`%T`).

## [0.0.4] - 2025-04-16

* Removed conflicting line in pyproject.toml - Programming Status :: Python :: 3.11

## [0.0.3] - 2025-04-16

* Added test cases
* Code cleanup
* Typehint fix

## [0.0.2] - 2025-04-15

* Removed unnecessary code

## [0.0.1] - 2025-04-15

* Initial release