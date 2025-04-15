#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import re
from typing import Match, Dict, List, Optional, Union, Any
from numbers import Number
from dataclasses import dataclass
from functools import lru_cache

try:
    from typing import Self  # Python 3.11+
except ImportError:
    from typing_extensions import Self  # Python <3.11

RE = {
    # Matches if type is NOT 'T' (type detection)
    'not_type': re.compile(r'[^T]'),
    # Matches if type is NOT 'v' (primitive value)
    'not_primitive': re.compile(r'[^v]'),
    # Matches numeric format specifiers
    'number': re.compile(r'[diefg]'),
    # Matches numeric argument types requiring number validation
    'numeric_arg': re.compile(r'[bcdiefguxX]'),
    # Matches JSON object specifier
    'json_object': re.compile(r'[j]'),
    # Matches plain text between format specifiers
    'plain_text': re.compile(r'^[^%]+'),
    # Matches double percent (escaped percent)
    'double_percent': re.compile(r'^%%'),
    # Matches format placeholder components
    'placeholder': re.compile(r"""
        ^%                # Starts with a percent sign
        (?:               # Non-capturing group for optional mapping key
            ([1-9]\d*)\$  # Positional argument number (e.g., 1$)
            |             # OR
            \(([^)]+)\)   # Mapping key (enclosed in parentheses)
        )?
        (\+)?             # Optional sign specifier (+)
        (0|'[^$])?        # Optional zero-padding or space-padding
        (-)?              # Optional left alignment (-)
        (\d+)?            # Optional minimum field width
        (?:               # Non-capturing group for optional precision
            \.            # Dot separator
            (\d*)         # Precision
        )?
        ([b-gijostTuvxX]) # Conversion type specifier
        """, re.VERBOSE),
    # Matches valid named argument keys
    'named_key': re.compile(r'^([a-z_][a-z_\d]*)', re.IGNORECASE),
    # Matches dot notation in named arguments
    'dot_access': re.compile(r'^\.([a-z_][a-z_\d]*)', re.IGNORECASE),
    # Matches array index access in named arguments
    'bracket_access': re.compile(r'^\[(\d+)\]'),
    # Matches numeric sign prefixes
    'numeral_prefix': re.compile(r'^[+-]'),
    # Matches allowed named key characters
    'allowed_named_key_chars': re.compile(r'^[a-zA-Z_][a-zA-Z0-9_]*$'),
    # Matches allowed numeric index
    'allowed_numeric_index': re.compile(r'^\d+$')
}

# Default configuration options
DEFAULT_OPTIONS: Dict = {
    'allow_computed_value': False,
    'throw_error_on_unmatched': False,
    'preserve_unmatched_placeholder': False,
}

# Constants for numeric operations
MAX_UINT32 = 0xFFFFFFFF
MAX_INT32 = 0x7FFFFFFF
MIN_INT32 = -0x80000000


@dataclass
class ParseTreeNode:
    placeholder: Optional[str] = None
    param_no: Optional[int] = None
    keys: Optional[List[str]] = None
    numeral_prefix: Optional[str] = None
    pad_char: Optional[str] = None
    align: Optional[bool] = None
    width: Optional[int] = None
    precision: Optional[int] = None
    type: Optional[str] = None


class ParseResult:
    def __init__(self, parse_tree: List[Union[str, ParseTreeNode]], 
                 named_used: bool = False, 
                 positional_used: bool = False):
        self.parse_tree = parse_tree
        self.named_used = named_used
        self.positional_used = positional_used


class PyPrintfConfig:
    """Chainable configuration object for sprintf."""
    def __init__(self, options: Optional[Dict[str, Any]] = None):
        self.options = DEFAULT_OPTIONS.copy()
        if options:
            self.validate_and_merge_options(options)
        self.stats = {
            'total_placeholders': 0,
            'total_named_placeholder': 0,
            'total_positional_placeholder': 0,
            'total_sequential_positional_placeholder': 0
        }

    def validate_and_merge_options(self, options: Dict[str, Any]):
        for key, value in options.items():
            if key not in self.options:
                raise KeyError(f"Invalid option: {key}")
            if not isinstance(value, type(self.options[key])):
                raise TypeError(f"Invalid type for option {key}")
            self.options[key] = value

    def sprintf(self, format_str: str, *args) -> str:
        """Format a string using the current configuration."""
        parse_result = sprintf_parse(format_str)
        return sprintf_format(
            parse_result.parse_tree, 
            args, 
            parse_result.named_used,
            self.options,
            self.stats
        )

    def vsprintf(self, format_str: str, argv) -> str:
        """Format a string using an array of arguments."""
        return self.sprintf(format_str, *argv) if argv else self.sprintf(format_str)

    def get_stats(self) -> Dict:
        """Get statistics about the formatting process."""
        return self.stats.copy()

    def allow_computed_value(self, value: bool) -> Self:
        self.options['allow_computed_value'] = bool(value)
        return self

    def throw_error_on_unmatched(self, value: bool) -> Self:
        self.options['throw_error_on_unmatched'] = bool(value)
        return self

    def preserve_unmatched_placeholder(self, value: bool) -> Self:
        self.options['preserve_unmatched_placeholder'] = bool(value)
        return self

@lru_cache(maxsize=128)
def sprintf_parse(format_str: str) -> ParseResult:
    """
    Parse a format string into an executable tree structure.

    Args:
        format_str: The format string to parse, following sprintf syntax.
        
    Returns:
        ParseResult: An object containing the parse tree and usage flags.
        
    Raises:
        SyntaxError: On invalid format syntax.
    """
    _format: str = format_str
    parse_tree: List = []
    named_used: bool = False
    positional_used: bool = False

    while _format:
        match: (Match[str] | None) = None
        
        # Match plain text between placeholders
        match = RE['plain_text'].match(_format)
        if match:
            parse_tree.append(match.group(0))
        else:
            # Match escaped percent (%%)
            match = RE['double_percent'].match(_format)
            if match:
                parse_tree.append('%')
            else:
                # Match complex placeholders
                match = RE['placeholder'].match(_format)
                if match:
                    # Handle named arguments
                    field_list = None
                    if match.group(2):
                        named_used = True
                        field_list: List = []
                        replacement_field = match.group(2)
                        
                        field_match = RE['named_key'].match(replacement_field)
                        if field_match:
                            if not RE['allowed_named_key_chars'].match(field_match.group(1)):
                                raise SyntaxError("[pyprintf] Invalid named argument key segment: must start with a letter or underscore, followed by letters, numbers, or underscores")
                            
                            field_list.append(field_match.group(1))
                            replacement_field = replacement_field[len(field_match.group(0)):]
                            
                            while replacement_field:
                                dot_match = RE['dot_access'].match(replacement_field)
                                if dot_match:
                                    if not RE['allowed_named_key_chars'].match(dot_match.group(1)):
                                        raise SyntaxError("[pyprintf] Invalid named argument key segment after dot: must start with a letter or underscore, followed by letters, numbers, or underscores")
                                    
                                    field_list.append(dot_match.group(1))
                                    replacement_field = replacement_field[len(dot_match.group(0)):]
                                else:
                                    bracket_match = RE['bracket_access'].match(replacement_field)
                                    if bracket_match:
                                        if not RE['allowed_numeric_index'].match(bracket_match.group(1)):
                                            raise SyntaxError("[pyprintf] Invalid array index in named argument key: must be a non-negative integer")
                                        
                                        field_list.append(bracket_match.group(1))
                                        replacement_field = replacement_field[len(bracket_match.group(0)):]
                                    else:
                                        raise SyntaxError("[pyprintf] failed to parse named argument key")
                        else:
                            raise SyntaxError("[pyprintf] failed to parse named argument key")
                    
                    # Handle positional arguments
                    elif match.group(1):  # Explicit positional placeholder
                        positional_used = True
                    else:  # Implicit positional placeholder
                        positional_used = True
                    
                    parse_tree.append(ParseTreeNode(
                        placeholder=match.group(0),
                        param_no=match.group(1),
                        keys=field_list,
                        numeral_prefix=match.group(3),
                        pad_char=match.group(4),
                        align=match.group(5),
                        width=match.group(6),
                        precision=match.group(7),
                        type=match.group(8)
                    ))
                else:
                    raise SyntaxError("[pyprintf] unexpected placeholder")
        
        if match:
            _format = _format[len(match.group(0)):]
        else:
            break

    return ParseResult(parse_tree, named_used, positional_used)


def sprintf_format(parse_tree: ParseTreeNode, argv: tuple, uses_named_args: bool, options: Dict, stats: Dict):
    """
    Core formatting engine that processes parsed format tree.

    Args:
        parse_tree: Result from sprintf_parse().
        argv: Values to format.
        uses_named_args: Whether the format string uses named arguments.
        options: Configuration options.
        stats: An object to collect statistics about the formatting process.
        
    Returns:
        str: Formatted string.
        
    Raises:
        TypeError: On invalid numeric arguments.
        Error: When accessing a property of an undefined named argument.
        SyntaxError: On missing arguments when options.throw_error_on_unmatched is true.
    """
    # If parse_tree is undefined, return empty string
    if not parse_tree:
        return ''

    cursor = 0
    tree_length = len(parse_tree)
    named_args = {}
    output = ''

    # Extract named arguments and filter positional arguments if named are used
    filtered_argv = []

    if uses_named_args:
        for arg in argv:
            if isinstance(arg, dict):
                named_args.update({k.lower(): v for k, v in arg.items()})
            else:
                filtered_argv.append(arg)
        
        # Use filtered_argv for positional parameters
        argv = filtered_argv

    for idx in range(tree_length):
        placeholder = parse_tree[idx]
        
        if isinstance(placeholder, str):
            output += placeholder
            continue
        
        arg = None
        
        stats['total_placeholders'] += 1
        
        # Get the argument value
        if placeholder.keys:
            arg = named_args
            preserved = False
            for k in range(len(placeholder.keys)):
                placeholder_key = placeholder.keys[k]
                try:
                    # Handle dictionary access
                    if isinstance(arg, dict):
                        arg = arg.get(placeholder_key)
                    else:
                        # Handle object attribute access
                        arg = getattr(arg, placeholder_key)
                except (KeyError, AttributeError, TypeError):
                    if options['preserve_unmatched_placeholder']:
                        arg = placeholder.placeholder
                        preserved = True
                        break
                    elif options['throw_error_on_unmatched']:
                        raise
                    else:
                        arg = None
                        break
                if arg is None:
                    if options['preserve_unmatched_placeholder']:
                        arg = placeholder.placeholder
                        preserved = True
                        break
                    elif options['throw_error_on_unmatched']:
                        raise ValueError(f"Missing value for key: {placeholder_key}")
                    else:
                        arg = 'undefined'
                        break
            # Preserve entire placeholder if any key was missing
            if options['preserve_unmatched_placeholder'] and not preserved and arg is None:
                arg = placeholder.placeholder
                
            stats['total_named_placeholder'] += 1
        
        elif placeholder.param_no:  # Explicit positional argument
            param_index = int(placeholder.param_no) - 1
            
            if options['throw_error_on_unmatched'] and param_index >= len(argv):
                raise ValueError(f"[pyprintf] Missing argument {placeholder.param_no}")
            
            try:
                arg = argv[param_index]
            except IndexError:
                if options['preserve_unmatched_placeholder']:
                    arg = placeholder.placeholder
                else:
                    arg = None
            
            stats['total_positional_placeholder'] += 1
        
        else:  # Implicit positional argument
            if options['throw_error_on_unmatched'] and cursor >= len(argv):
                raise ValueError("[pyprintf] Too few arguments")
            
            try:
                arg = argv[cursor]
                cursor += 1
            except IndexError:
                if options['preserve_unmatched_placeholder']:
                    arg = placeholder.placeholder
                else:
                    arg = None
            
            stats['total_sequential_positional_placeholder'] += 1
        
        # Handle function arguments for non-type/non-primitive specifiers
        is_function_arg = (RE['not_type'].search(placeholder.type) and 
                          RE['not_primitive'].search(placeholder.type) and 
                          callable(arg))
        
        if not options['allow_computed_value'] and is_function_arg:
            raise ValueError("[pyprintf] Function arguments are not allowed by default. Enable with config().allow_computed_value(True)")
        
        if options['allow_computed_value'] and is_function_arg:
            try:
                arg = arg()
            except Exception:
                raise ValueError("[pyprintf] Failed to execute function argument")
        
        # Validate numeric arguments for numeric placeholders
        if RE['numeric_arg'].search(placeholder.type):
            if arg is not None and not (isinstance(arg, (int, float)) or isinstance(arg, str) and arg.isdigit()):
                try:
                    # Try to convert to float
                    float(arg)
                except (ValueError, TypeError):
                    raise TypeError(f"[pyprintf] expecting number but found {type(arg).__name__}")
        
        is_positive = None
        numeral_prefix = ''
        
        # Format according to type
        if RE['number'].search(placeholder.type):
            try:
                is_positive = float(arg) >= 0 if arg is not None else True
            except (ValueError, TypeError):
                is_positive = True
        
        # Process argument based on format specifier
        if placeholder.type == 'b':  # Binary
            try:
                arg = bin(int(arg))[2:]  # Remove '0b' prefix
            except (ValueError, TypeError):
                arg = '0'
        
        elif placeholder.type == 'c':  # Character
            try:
                arg = chr(int(arg))
            except (ValueError, TypeError, OverflowError):
                arg = '\0'
        
        elif placeholder.type in ('d', 'i'):  # Integer
            if isinstance(arg, Number):
                arg = str(int(arg))
            elif isinstance(arg, str) and arg.isdigit():
                arg = str(int(arg))
            else:
                arg = '0'
        
        elif placeholder.type == 'j':
            indent = int(placeholder.width) if placeholder.width else None
            try:
                arg = json.dumps(arg, indent=indent if not indent else None)
            except:
                arg = 'null'
        
        elif placeholder.type == 'e':  # Exponential notation
            try:
                if placeholder.precision:
                    try:
                        precision = int(placeholder.precision) if placeholder.precision else 6
                    except ValueError:
                        precision = 6

                    arg = f"{float(arg):.{precision}e}"
                else:
                    arg = f"{float(arg):.6e}"
            except (ValueError, TypeError):
                arg = '0.000000e+00'

        elif placeholder.type == 'f':
            try:
                # Handle precision specification
                if placeholder.precision == '':  # Explicit empty precision (%.f)
                    precision = 0
                else:
                    precision = int(placeholder.precision) if placeholder.precision else 6
                
                formatted = f"{float(arg):.{precision}f}"
                
                # Remove decimal point for zero precision
                if precision == 0:
                    formatted = formatted.split('.')[0]
                
                arg = formatted
            except:
                arg = '0' if precision == 0 else '0.000000'

        elif placeholder.type == 'g':  # General format
            try:
                if placeholder.precision:
                    # Use Python's %g format
                    arg = f"{float(arg):.{placeholder.precision}g}"
                else:
                    arg = str(float(arg))
            except (ValueError, TypeError):
                arg = '0'
        
        elif placeholder.type == 'o':
            try:
                num = int(arg)
                num_uint32 = num & 0xFFFFFFFF  # Convert to unsigned 32-bit
                arg = oct(num_uint32)[2:]
            except:
                arg = '0'
        
        elif placeholder.type == 's':  # String
            arg = str(arg) if arg is not None else 'None'
            if placeholder.precision:
                arg = arg[:int(placeholder.precision)]
        
        elif placeholder.type == 't':
            arg = str(arg).lower()
            if placeholder.precision:
                arg = arg[:int(placeholder.precision)]
        
        elif placeholder.type == 'T':  # Type detection
            arg = type(arg).__name__.lower() if arg is not None else 'nonetype'
            if placeholder.precision:
                arg = arg[:int(placeholder.precision)]
        
        elif placeholder.type == 'u':  # Unsigned integer
            try:
                arg = str(int(arg) & MAX_UINT32)
            except (ValueError, TypeError):
                arg = '0'
        
        elif placeholder.type == 'v':  # Primitive value
            arg = str(arg) if arg is not None else 'None'
            
            if placeholder.precision:
                arg = arg[:int(placeholder.precision)]
        
        elif placeholder.type in ('x', 'X'):
            try:
                num = int(arg)
                # Handle 32-bit unsigned conversion for negative numbers only
                if num < 0:
                    num = num & 0xFFFFFFFF
                
                # Format with original value for positive numbers
                width = int(placeholder.width) if placeholder.width else 0
                fmt = f"{{:0{width}x}}" if width else "{:x}"
                hex_str = fmt.format(num)

                # Handle large positive numbers (>32 bits)
                if num > 0xFFFFFFFF and width == 0:
                    # Format as 64-bit with leading zeros stripped
                    hex_str = f"{num:016x}".lstrip('0')
                    if not hex_str:  # Handle zero case
                        hex_str = '0'

                hex_str = hex_str.upper() if placeholder.type == 'X' else hex_str
                arg = hex_str
            except (ValueError, TypeError):
                arg = '0'
        
        else:
            raise ValueError(f"[pyprintf] Unknown type: {placeholder.type}")
        
        # Apply padding and alignment
        if RE['json_object'].search(placeholder.type):
            output += arg
        else:
            # Handle numeric sign prefix
            if RE['number'].search(placeholder.type) and arg is not None and (not is_positive or placeholder.numeral_prefix):
                numeral_prefix = '+' if is_positive else '-'
                # Remove any existing sign from the formatted arg
                arg = arg.lstrip('+-')
            
            pad_character = ' '
            if placeholder.pad_char:
                if placeholder.pad_char == '0':
                    pad_character = '0'
                elif len(placeholder.pad_char) > 1:
                    pad_character = placeholder.pad_char[1]
            
            width = int(placeholder.width) if placeholder.width else 0
            pad_length = width - len(numeral_prefix + arg)
            pad = pad_character * pad_length if width and pad_length > 0 else ''
            
            if placeholder.align:  # Left align
                output += numeral_prefix + arg + pad
            else:  # Right align
                if pad_character == '0':
                    output += numeral_prefix + pad + arg
                else:
                    output += pad + numeral_prefix + arg

    return output


def sprintf(format_str: str, *args) -> str:
    """
    Main formatting function similar to C's sprintf

    Args:
        format_str: Format string containing placeholders
        *args: Values to format
        
    Returns:
        str: Formatted string
    """
    options: Dict = DEFAULT_OPTIONS.copy()
    stats: Dict = {
        'total_placeholders': 0,
        'total_named_placeholder': 0,
        'total_positional_placeholder': 0,
        'total_sequential_positional_placeholder': 0
    }

    parse_result = sprintf_parse(format_str)

    return sprintf_format(parse_result.parse_tree, args, parse_result.named_used, options, stats)


def vsprintf(format_str: str, argv) -> str:
    """
    Version of sprintf that accepts arguments as a list

    Args:
        format_str: Format string
        argv: List of values to format
        
    Returns:
        str: Formatted string
    """
    if argv is None:
        argv = []

    return sprintf(format_str, *argv)


def config(options: Dict | None = None) -> PyPrintfConfig:
    """
    Creates a chainable configuration object for sprintf

    Args:
        options: Configuration options
        
    Returns:
        PyPrintfConfig: A chainable configuration object
    """
    return PyPrintfConfig(options)


class Sprintf:
    def __init__(self):
        self._config = PyPrintfConfig()

    def __call__(self, format_str: str, *args) -> str:
        return self._config.sprintf(format_str, *args)

    @property
    def config(self) -> PyPrintfConfig:
        return self._config

    def vsprintf(self, format_str: str, argv) -> str:
        return self._config.vsprintf(format_str, argv)

# Create singleton instances
sprintf = Sprintf()
vsprintf = sprintf.vsprintf