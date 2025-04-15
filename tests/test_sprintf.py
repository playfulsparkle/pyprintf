import pytest
from pyprintf import sprintf, PyPrintfConfig
import json
import math

class TestPyPrintf:
    @pytest.fixture
    def config(self):
        return PyPrintfConfig()

    def test_percentage_sign(self):
        assert sprintf("%%") == "%"

    def test_binary_number(self):
        assert sprintf("%b", 2) == "10"

    def test_character(self):
        assert sprintf("%c", 65) == "A"

    def test_decimal_integer(self):
        assert sprintf("%d", 2) == "2"
        assert sprintf("%d", "2") == "2"

    def test_integer(self):
        assert sprintf("%i", 2) == "2"
        assert sprintf("%i", "2") == "2"

    def test_json(self):
        assert sprintf("%j", {"foo": "bar"}) == json.dumps({"foo": "bar"})
        assert sprintf("%j", ["foo", "bar"]) == json.dumps(["foo", "bar"])

    def test_scientific_notation(self):
        assert sprintf("%e", 2) == "2.000000e+00"

    def test_unsigned_decimal(self):
        assert sprintf("%u", 2) == "2"
        assert sprintf("%u", -2) == "4294967294"

    def test_float(self):
        assert sprintf("%f", 2.2) == "2.200000"

    def test_shortest_notation(self):
        assert sprintf("%g", math.pi) == "3.141592653589793"

    def test_octal(self):
        assert sprintf("%o", 8) == "10"
        assert sprintf("%o", -8) == "37777777770"

    def test_string(self):
        assert sprintf("%s", "%s") == "%s"

    def test_hexadecimal(self):
        assert sprintf("%x", 255) == "ff"
        assert sprintf("%x", -255) == "ffffff01"
        assert sprintf("%X", 255) == "FF"
        assert sprintf("%X", -255) == "FFFFFF01"

    def test_positional_arguments(self):
        assert sprintf("%2$s %3$s a %1$s", "cracker", "Polly", "wants") == "Polly wants a cracker"

    def test_named_arguments(self):
        assert sprintf("Hello %(who)s!", {"who": "world"}) == "Hello world!"

    class TestCallbackFunctions:
        def test_callback_string(self):
            cfg = PyPrintfConfig().allow_computed_value(True)
            assert cfg.sprintf("%s", lambda: "foobar") == "foobar"

        def test_callback_float_precision(self):
            cfg = PyPrintfConfig().allow_computed_value(True)
            assert cfg.sprintf("%.1f", lambda: 2.345) == "2.3"

        def test_callback_json_indentation(self):
            cfg = PyPrintfConfig().allow_computed_value(True)
            result = cfg.sprintf("%2j", lambda: {"foo": "bar"})
            expected = json.dumps({"foo": "bar"})
            assert result == expected

        def test_callback_shortest_notation(self):
            cfg = PyPrintfConfig().allow_computed_value(True)
            assert cfg.sprintf("%g", lambda: math.pi) == "3.141592653589793"

        def test_callback_octal(self):
            cfg = PyPrintfConfig().allow_computed_value(True)
            assert cfg.sprintf("%o", lambda: 8) == "10"

        def test_callback_unsigned_decimal(self):
            cfg = PyPrintfConfig().allow_computed_value(True)
            assert cfg.sprintf("%u", lambda: 2) == "2"

        def test_callback_large_unsigned(self):
            cfg = PyPrintfConfig().allow_computed_value(True)
            assert cfg.sprintf("%u", lambda: -2) == "4294967294"

        def test_callback_hex_lowercase(self):
            cfg = PyPrintfConfig().allow_computed_value(True)
            assert cfg.sprintf("%x", lambda: 255) == "ff"
            assert cfg.sprintf("%x", lambda: -255) == "ffffff01"

        def test_callback_hex_uppercase(self):
            cfg = PyPrintfConfig().allow_computed_value(True)
            assert cfg.sprintf("%X", lambda: 255) == "FF"
            assert cfg.sprintf("%X", lambda: -255) == "FFFFFF01"

        def test_callback_large_hex(self):
            cfg = PyPrintfConfig().allow_computed_value(True)
            assert cfg.sprintf("%X", lambda: 150460469257) == "2308249009"

        def test_callback_binary(self):
            cfg = PyPrintfConfig().allow_computed_value(True)
            assert cfg.sprintf("%b", lambda: 2) == "10"

        def test_callback_character(self):
            cfg = PyPrintfConfig().allow_computed_value(True)
            assert cfg.sprintf("%c", lambda: 65) == "A"

        def test_callback_type_detection(self):
            assert sprintf("%T", lambda: None) == "function"

        def test_callback_value_formatting(self):
            result = sprintf("%v", lambda: 42)
            assert "lambda" in result  # Python shows <lambda> in repr

        def test_callback_security(self):
            cfg = PyPrintfConfig().allow_computed_value(False)
            with pytest.raises(ValueError):
                cfg.sprintf("%s", lambda: "dangerous")

    class TestBooleanFormatting:
        def test_boolean_values(self):
            assert sprintf("%t", True) == "true"
            assert sprintf("%.1t", True) == "t"
            assert sprintf("%t", False) == "false"
            assert sprintf("%.1t", False) == "f"

    class TestTypeDetection:
        def test_type_formatting(self):
            assert sprintf("%T", None) == "nonetype"
            assert sprintf("%T", True) == "bool"
            assert sprintf("%T", 42) == "int"
            assert sprintf("%T", "string") == "str"
            assert sprintf("%T", [1,2,3]) == "list"
            assert sprintf("%T", {"key": "value"}) == "dict"

    class TestValueFormatting:
        def test_value_formatting(self):
            assert sprintf("%v", True) == "True"
            assert sprintf("%v", 42) == "42"
            assert sprintf("%v", [1,2,3]) == "[1, 2, 3]"

    class TestComplexFormatting:
        def test_sign_handling(self):
            assert sprintf("%+d", 2) == "+2"
            assert sprintf("%+d", -2) == "-2"
            assert sprintf("%+.1f", -2.34) == "-2.3"

        def test_padding(self):
            assert sprintf("%05d", -2) == "-0002"
            assert sprintf("%5s", "<") == "    <"
            assert sprintf("%-5s", ">") == ">    "

        def test_precision(self):
            assert sprintf("%.1f", 2.345) == "2.3"
            assert sprintf("%5.5s", "xxxxxx") == "xxxxx"

    class TestConfiguration:
        def test_preserve_unmatched(self):
            cfg = PyPrintfConfig().preserve_unmatched_placeholder(True)
            assert cfg.sprintf('%(name)s number 1') == "%(name)s number 1"

        def test_stats_tracking(self):
            cfg = PyPrintfConfig()
            cfg.sprintf("%s %s %s %s %(name)s %1$s %2$s")
            stats = cfg.get_stats()
            assert stats['total_placeholders'] == 7
            assert stats['total_named_placeholder'] == 1

    class TestEdgeCases:
        def test_large_numbers(self):
            assert sprintf("%d", 9999999999999999999999999999999999999999) == "9999999999999999999999999999999999999999"

        def test_precision_handling(self):
            assert sprintf("%.f", 2) == "2"
            assert sprintf("%.99f", 1).startswith("1.000000")

    class TestErrorHandling:
        def test_missing_arguments(self):
            cfg = PyPrintfConfig().throw_error_on_unmatched(True)
            with pytest.raises(ValueError):  # Now matches implementation
                cfg.sprintf("%s %s", "single")

        def test_invalid_format(self):
            cfg = PyPrintfConfig().throw_error_on_unmatched(True)
            with pytest.raises(ValueError):
                cfg.sprintf("%invalid")

if __name__ == "__main__":
    pytest.main()