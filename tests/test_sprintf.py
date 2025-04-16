import pytest
from src.pyprintf import sprintf, config
import json
import math


class TestSimplePlaceholders:
    def test_should_format_correctly_unmatched_placeholder(self):
        cfg = config().preserve_unmatched_placeholder(True)
        firstPass = cfg.sprintf(
            "My name is %(firstname)s %(lastname)s", {"lastname": "Doe"}
        )

        assert firstPass == "My name is %(firstname)s Doe"

        assert cfg.sprintf(firstPass, {"firstname": "John"}) == "My name is John Doe"

    def test_should_format_a_percentage_sign(self):
        assert sprintf("%%") == "%"

    def test_should_format_a_binary_number(self):
        assert sprintf("%b", 2) == "10"

    def test_should_format_a_character(self):
        assert sprintf("%c", 65) == "A"

    def test_should_format_a_decimal_integer(self):
        assert sprintf("%d", 2) == "2"

    def test_should_format_an_integer(self):
        assert sprintf("%i", 2) == "2"

    def test_should_format_a_decimal_integer_from_a_string(self):
        assert sprintf("%d", "2") == "2"

    def test_should_format_an_integer_from_a_string(self):
        assert sprintf("%i", "2") == "2"

    def test_should_format_a_json_object(self):
        assert sprintf("%j", {"foo": "bar"}) == json.dumps({"foo": "bar"})

    def test_should_format_a_json_array(self):
        assert sprintf("%j", ["foo", "bar"]) == json.dumps(["foo", "bar"])

    def test_should_format_a_number_in_scientific_notation_lowercase(self):
        assert sprintf("%e", 2) == "2e+0"

    def test_should_format_an_unsigned_decimal_integer(self):
        assert sprintf("%u", 2) == "2"

    def test_should_format_a_large_unsigned_decimal_integer_from_a_negative_number(
        self,
    ):
        assert sprintf("%u", -2) == "4294967294"

    def test_should_format_a_floating_point_number(self):
        assert sprintf("%f", 2.2) == "2.2"

    def test_should_format_a_number_in_shortest_notation_lowercase(self):
        assert sprintf("%g", math.pi) == "3.141592653589793"

    def test_should_format_an_octal_number(self):
        assert sprintf("%o", 8) == "10"

    def test_should_format_a_large_octal_number_from_a_negative_number(self):
        assert sprintf("%o", -8) == "37777777770"

    def test_should_format_a_string(self):
        assert sprintf("%s", "%s") == "%s"

    def test_should_format_a_hexadecimal_number_lowercase(self):
        assert sprintf("%x", 255) == "ff"

    def test_should_format_a_large_hexadecimal_number_lowercase_from_a_negative_number(
        self,
    ):
        assert sprintf("%x", -255) == "ffffff01"

    def test_should_format_a_hexadecimal_number_uppercase(self):
        assert sprintf("%X", 255) == "FF"

    def test_should_format_a_large_hexadecimal_number_uppercase_from_a_negative_number(
        self,
    ):
        assert sprintf("%X", -255) == "FFFFFF01"

    def test_should_format_arguments_by_index(self):
        assert (
            sprintf("%2$s %3$s a %1$s", "cracker", "Polly", "wants")
            == "Polly wants a cracker"
        )

    def test_should_format_arguments_by_name(self):
        assert sprintf("Hello %(who)s!", {"who": "world"}) == "Hello world!"

    def test_should_format_named_and_positional_arguments(self):
        assert (
            sprintf("%(name)s %s a %s", "wants", "cracker", {"name": "Polly"})
            == "Polly wants a cracker"
        )

    def test_should_format_named_and_positional_index_arguments(self):
        assert (
            sprintf("%(name)s %2$s a %1$s", "cracker", "wants", {"name": "Polly"})
            == "Polly wants a cracker"
        )


class TestPlaceholderBoolean:
    def test_should_format_true_as_true(self):
        assert sprintf("%t", True) == "true"

    def test_should_format_true_as_t_with_precision_1(self):
        assert sprintf("%.1t", True) == "t"

    def test_should_format_the_string_true_as_true(self):
        assert sprintf("%t", "True") == "true"

    def test_should_format_the_number_1_as_true(self):
        assert sprintf("%t", 1) == "true"

    def test_should_format_false_as_false(self):
        assert sprintf("%t", False) == "false"

    def test_should_format_false_as_f_with_precision_1(self):
        assert sprintf("%.1t", False) == "f"

    def test_should_format_an_empty_string_as_false(self):
        assert sprintf("%t", "") == "false"

    def test_should_format_the_number_0_as_false(self):
        assert sprintf("%t", "") == "false"


class TestPlaceholderType:
    def test_should_format_none_as_nonetype(self):
        assert sprintf("%T", None) == "nonetype"

    def test_should_format_a_boolean_as_boolean(self):
        assert sprintf("%T", True) == "bool"

    def test_should_format_a_number_as_number(self):
        assert sprintf("%T", 42) == "int"

    def test_should_format_a_string_as_string(self):
        assert sprintf("%T", "This is a string") == "str"

    def test_should_format_a_list_as_list(self):
        assert sprintf("%T", [1, 2, 3]) == "list"

    def test_should_format_a_dictionary_as_dict(self):
        assert sprintf("%T", {"key": "value"}) == "dict"


class TestSignFormatting:
    def test_should_format_a_positive_decimal_integer_without_a_sign(self):
        assert sprintf("%d", 2) == "2"

    def test_should_format_a_negative_decimal_integer_with_a_minus_sign(self):
        assert sprintf("%d", -2) == "-2"

    def test_should_format_a_positive_decimal_integer_with_a_plus_sign(self):
        assert sprintf("%+d", 2) == "+2"

    def test_should_format_a_negative_decimal_integer_with_a_minus_sign_forced(self):
        assert sprintf("%+d", -2) == "-2"

    def test_should_format_a_positive_integer_without_a_sign(self):
        assert sprintf("%i", 2) == "2"

    def test_should_format_a_negative_integer_with_a_minus_sign(self):
        assert sprintf("%i", -2) == "-2"

    def test_should_format_a_positive_integer_with_a_plus_sign(self):
        assert sprintf("%+i", 2) == "+2"

    def test_should_format_a_negative_integer_with_a_minus_sign_forced(self):
        assert sprintf("%+i", -2) == "-2"

    def test_should_format_a_positive_float_without_a_sig(self):
        assert sprintf("%f", 2.2) == "2.2"

    def test_should_format_a_negative_float_with_a_minus_sign(self):
        assert sprintf("%f", -2.2) == "-2.2"

    def test_should_format_a_positive_float_with_a_plus_sign(self):
        assert sprintf("%+f", 2.2) == "+2.2"

    def test_should_format_a_negative_float_with_a_minus_sign_forced(self):
        assert sprintf("%+f", -2.2) == "-2.2"

    def test_should_format_a_negative_float_with_a_plus_sign_and_precision(self):
        assert sprintf("%+.1f", -2.34) == "-2.3"

    def test_should_format_a_negative_zero_float_with_a_plus_sign_and_precision(self):
        assert sprintf("%+.1f", -0.01) == "-0.0"

    def test_should_format_pi_with_shortest_notation_and_precision(self):
        assert sprintf("%.6g", math.pi) == "3.14159"

    def test_should_format_pi_with_shortest_notation_and_different_precision(self):
        assert sprintf("%.3g", math.pi) == "3.14"

    def test_should_format_pi_with_shortest_notation_and_another_precision(self):
        assert sprintf("%.1g", math.pi) == "3"

    def test_should_format_a_negative_number_with_leading_zeros_and_a_plus_sign(self):
        assert sprintf("%+010d", -123) == "-000000123"

    def test_should_format_a_negative_number_with_custom_padding_and_a_plus_sign(self):
        assert sprintf("%+'_10d", -123) == "______-123"

    def test_should_format_multiple_floats_with_different_signs(self):
        assert sprintf("%f %f", -234.34, 123.2) == "-234.34 123.2"


if __name__ == "__main__":
    pytest.main()
