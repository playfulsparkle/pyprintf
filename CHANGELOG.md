# Change Log

All notable changes to the pyprintf project will be documented in this file.

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