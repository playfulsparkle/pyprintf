import pytest
from pyprintf import sprintf, config
import json
import math


class TestSimplePlaceholders:
    def test_format_correctly_unmatched_placeholder(self):
        cfg = config().preserve_unmatched_placeholder(True)
        firstPass = cfg.sprintf(
            "My name is %(firstname)s %(lastname)s", {"lastname": "Doe"}
        )

        assert firstPass == "My name is %(firstname)s Doe"

        assert cfg.sprintf(firstPass, {"firstname": "John"}) == "My name is John Doe"

    def test_format_a_percentage_sign(self):
        assert sprintf("%%") == "%"

    def test_format_a_binary_number(self):
        assert sprintf("%b", 2) == "10"

    def test_format_a_character(self):
        assert sprintf("%c", 65) == "A"

    def test_format_a_decimal_integer(self):
        assert sprintf("%d", 2) == "2"

    def test_format_an_integer(self):
        assert sprintf("%i", 2) == "2"

    def test_format_a_decimal_integer_from_a_string(self):
        assert sprintf("%d", "2") == "2"

    def test_format_an_integer_from_a_string(self):
        assert sprintf("%i", "2") == "2"

    def test_format_a_json_object(self):
        assert sprintf("%j", {"foo": "bar"}) == json.dumps({"foo": "bar"})

    def test_format_a_json_array(self):
        assert sprintf("%j", ["foo", "bar"]) == json.dumps(["foo", "bar"])

    def test_format_a_number_in_scientific_notation_lowercase(self):
        assert sprintf("%e", 2) == "2e+0"

    def test_format_an_unsigned_decimal_integer(self):
        assert sprintf("%u", 2) == "2"

    def test_format_a_large_unsigned_decimal_integer_from_a_negative_number(
        self,
    ):
        assert sprintf("%u", -2) == "4294967294"

    def test_format_a_floating_point_number(self):
        assert sprintf("%f", 2.2) == "2.2"

    def test_format_a_number_in_shortest_notation_lowercase(self):
        assert sprintf("%g", math.pi) == "3.141592653589793"

    def test_format_an_octal_number(self):
        assert sprintf("%o", 8) == "10"

    def test_format_a_large_octal_number_from_a_negative_number(self):
        assert sprintf("%o", -8) == "37777777770"

    def test_format_a_string(self):
        assert sprintf("%s", "%s") == "%s"

    def test_format_a_hexadecimal_number_lowercase(self):
        assert sprintf("%x", 255) == "ff"

    def test_format_a_large_hexadecimal_number_lowercase_from_a_negative_number(
        self,
    ):
        assert sprintf("%x", -255) == "ffffff01"

    def test_format_a_hexadecimal_number_uppercase(self):
        assert sprintf("%X", 255) == "FF"

    def test_format_a_large_hexadecimal_number_uppercase_from_a_negative_number(
        self,
    ):
        assert sprintf("%X", -255) == "FFFFFF01"

    def test_format_arguments_by_index(self):
        assert (
            sprintf("%2$s %3$s a %1$s", "cracker", "Polly", "wants")
            == "Polly wants a cracker"
        )

    def test_format_arguments_by_name(self):
        assert sprintf("Hello %(who)s!", {"who": "world"}) == "Hello world!"

    def test_format_named_and_positional_arguments(self):
        assert (
            sprintf("%(name)s %s a %s", "wants", "cracker", {"name": "Polly"})
            == "Polly wants a cracker"
        )

    def test_format_named_and_positional_index_arguments(self):
        assert (
            sprintf("%(name)s %2$s a %1$s", "cracker", "wants", {"name": "Polly"})
            == "Polly wants a cracker"
        )


class TestPlaceholderBoolean:
    def test_format_true_as_true(self):
        assert sprintf("%t", True) == "True"

    def test_format_true_as_t_with_precision_1(self):
        assert sprintf("%.1t", True) == "T"

    def test_format_the_string_true_as_true(self):
        assert sprintf("%t", "True") == "True"

    def test_format_the_number_1_as_true(self):
        assert sprintf("%t", 1) == "True"

    def test_format_false_as_false(self):
        assert sprintf("%t", False) == "False"

    def test_format_false_as_f_with_precision_1(self):
        assert sprintf("%.1t", False) == "F"

    def test_format_an_empty_string_as_false(self):
        assert sprintf("%t", "") == "False"

    def test_format_the_number_0_as_false(self):
        assert sprintf("%t", "") == "False"


class TestPlaceholderType:
    def test_format_none_as_nonetype(self):
        assert sprintf("%T", None) == "NoneType"

    def test_format_a_boolean_as_boolean(self):
        assert sprintf("%T", True) == "bool"

    def test_format_a_number_as_number(self):
        assert sprintf("%T", 42) == "int"

    def test_format_a_string_as_string(self):
        assert sprintf("%T", "This is a string") == "str"

    def test_format_a_list_as_list(self):
        assert sprintf("%T", [1, 2, 3]) == "list"

    def test_format_a_dictionary_as_dict(self):
        assert sprintf("%T", {"key": "value"}) == "dict"


class TestSignFormatting:
    def test_format_a_positive_decimal_integer_without_a_sign(self):
        assert sprintf("%d", 2) == "2"

    def test_format_a_negative_decimal_integer_with_a_minus_sign(self):
        assert sprintf("%d", -2) == "-2"

    def test_format_a_positive_decimal_integer_with_a_plus_sign(self):
        assert sprintf("%+d", 2) == "+2"

    def test_format_a_negative_decimal_integer_with_a_minus_sign_forced(self):
        assert sprintf("%+d", -2) == "-2"

    def test_format_a_positive_integer_without_a_sign(self):
        assert sprintf("%i", 2) == "2"

    def test_format_a_negative_integer_with_a_minus_sign(self):
        assert sprintf("%i", -2) == "-2"

    def test_format_a_positive_integer_with_a_plus_sign(self):
        assert sprintf("%+i", 2) == "+2"

    def test_format_a_negative_integer_with_a_minus_sign_forced(self):
        assert sprintf("%+i", -2) == "-2"

    def test_format_a_positive_float_without_a_sig(self):
        assert sprintf("%f", 2.2) == "2.2"

    def test_format_a_negative_float_with_a_minus_sign(self):
        assert sprintf("%f", -2.2) == "-2.2"

    def test_format_a_positive_float_with_a_plus_sign(self):
        assert sprintf("%+f", 2.2) == "+2.2"

    def test_format_a_negative_float_with_a_minus_sign_forced(self):
        assert sprintf("%+f", -2.2) == "-2.2"

    def test_format_a_negative_float_with_a_plus_sign_and_precision(self):
        assert sprintf("%+.1f", -2.34) == "-2.3"

    def test_format_a_negative_zero_float_with_a_plus_sign_and_precision(self):
        assert sprintf("%+.1f", -0.01) == "-0.0"

    def test_format_pi_with_shortest_notation_and_precision(self):
        assert sprintf("%.6g", math.pi) == "3.14159"

    def test_format_pi_with_shortest_notation_and_different_precision(self):
        assert sprintf("%.3g", math.pi) == "3.14"

    def test_format_pi_with_shortest_notation_and_another_precision(self):
        assert sprintf("%.1g", math.pi) == "3"

    def test_format_a_negative_number_with_leading_zeros_and_a_plus_sign(self):
        assert sprintf("%+010d", -123) == "-000000123"

    def test_format_a_negative_number_with_custom_padding_and_a_plus_sign(self):
        assert sprintf("%+'_10d", -123) == "______-123"

    def test_format_multiple_floats_with_different_signs(self):
        assert sprintf("%f %f", -234.34, 123.2) == "-234.34 123.2"


class TestPadding:
    def test_pad_a_negative_number_with_leading_zeros(self):
        assert sprintf("%05d", -2) == "-0002"

    def test_pad_a_negative_integer_with_leading_zeros(self):
        assert sprintf("%05i", -2) == "-0002"

    def test_pad_a_string_with_leading_spaces(self):
        assert sprintf("%5s", "<") == "    <"

    def test_pad_a_string_with_leading_zeros(self):
        assert sprintf("%05s", "<") == "0000<"

    def test_pad_a_string_with_leading_underscores(self):
        assert sprintf("%'_5s", "<") == "____<"

    def test_pad_a_string_with_trailing_spaces(self):
        assert sprintf("%-5s", ">") == ">    "

    def test_pad_a_string_with_trailing_zeros_ignored(self):
        assert sprintf("%0-5s", ">") == ">0000"

    def test_pad_a_string_with_trailing_underscores_ignored(self):
        assert sprintf("%'_-5s", ">") == ">____"

    def test_not_pad_a_string_longer_than_the_specified_width(self):
        assert sprintf("%5s", "xxxxxx") == "xxxxxx"

    def test_not_pad_an_unsigned_integer_beyond_its_length(self):
        assert sprintf("%02u", 1234) == "1234"

    def test_pad_a_float_with_leading_spaces_and_specify_precision(self):
        assert sprintf("%8.3f", -10.23456) == " -10.235"

    def test_format_a_float_and_a_string_with_padding(self):
        assert sprintf("%f %s", -12.34, "xxx") == "-12.34 xxx"

    def test_format_a_json_object_with_indentation(self):
        assert sprintf("%2j", {"foo": "bar"}) == json.dumps({"foo": "bar"})

    def test_format_a_json_array_with_indentation(self):
        assert sprintf("%2j", ["foo", "bar"]) == '["foo", "bar"]'


class TestPrecision:
    def test_format_a_float_with_specified_precision(self):
        assert sprintf("%.1f", 2.345) == "2.3"

    def test_limit_the_length_of_a_string_with_precision(self):
        assert sprintf("%5.5s", "xxxxxx") == "xxxxx"

    def test_limit_the_length_of_a_padded_string_with_precision(self):
        assert sprintf("%5.1s", "xxxxxx") == "    x"


class TestLambda:
    def test_format_a_string_using_lambda(self):
        cfg = config().allow_computed_value(True)
        assert cfg.sprintf("%s", lambda: "foobar") == "foobar"

    def test_format_a_float_with_specified_precision_using_lambda(self):
        cfg = config().allow_computed_value(True)
        assert cfg.sprintf("%.1f", lambda: 2.345) == "2.3"

    def test_format_a_json_object_with_indentation_using_lambda(self):
        cfg = config().allow_computed_value(True)
        assert cfg.sprintf("%2j", lambda: {"foo": "bar"}) == json.dumps({"foo": "bar"})

    def test_format_a_number_in_shortest_notation_lowercase_using_lambda(self):
        cfg = config().allow_computed_value(True)
        assert cfg.sprintf("%g", lambda: math.pi) == "3.141592653589793"

    def test_format_an_octal_number_using_lambda(self):
        cfg = config().allow_computed_value(True)
        assert cfg.sprintf("%o", lambda: 8) == "10"

    def test_format_an_unsigned_decimal_integer_using_lambda(self):
        cfg = config().allow_computed_value(True)
        assert cfg.sprintf("%u", lambda: 2) == "2"

    def test_format_a_large_unsigned_decimal_integer_from_a_negative_number_using_lambda(
        self,
    ):
        cfg = config().allow_computed_value(True)
        assert cfg.sprintf("%u", lambda: -2) == "4294967294"

    def test_format_a_hexadecimal_number_lowercase_using_lambda(self):
        cfg = config().allow_computed_value(True)
        assert cfg.sprintf("%x", lambda: 255) == "ff"

    def test_format_a_large_hexadecimal_number_lowercase_from_a_negative_number_using_lambda(
        self,
    ):
        cfg = config().allow_computed_value(True)
        assert cfg.sprintf("%x", lambda: -255) == "ffffff01"

    def test_format_a_hexadecimal_number_uppercase_using_using_lambda(self):
        cfg = config().allow_computed_value(True)
        assert cfg.sprintf("%X", lambda: 255) == "FF"

    def test_format_a_large_hexadecimal_number_uppercase_from_a_negative_number_using_lambda(
        self,
    ):
        cfg = config().allow_computed_value(True)
        assert cfg.sprintf("%X", lambda: -255) == "FFFFFF01"

    def test_format_a_large_number_exceeding_32_bits_correctly_as_a_hexadecimal_string_using_lambda(
        self,
    ):
        cfg = config().allow_computed_value(True)
        assert cfg.sprintf("%X", lambda: 150460469257) == "2308249009"

    def test_format_a_binary_number_using_lambda(self):
        cfg = config().allow_computed_value(True)
        assert cfg.sprintf("%b", lambda: 2) == "10"

    def test_format_a_character_using_lambda(self):
        cfg = config().allow_computed_value(True)
        assert cfg.sprintf("%c", lambda: 65) == "A"

    def test_format_undefined_as_function_using_lambda(self):
        assert sprintf("%T", lambda: None) == "function"


class TestOther:
    def test_format_a_bigint_value_correctly_as_a_decimal_string(self):
        assert (
            sprintf("%d", 9999999999999999999999999999999999999999)
            == "9999999999999999999999999999999999999999"
        )
        assert (
            sprintf("%i", 9999999999999999999999999999999999999999)
            == "9999999999999999999999999999999999999999"
        )

    def test_treat_f_as_having_zero_precision_for_floating_point_formatting(self):
        assert sprintf("%.f", 2) == "2"
        assert sprintf("%.0f", 2) == "2"

    def test_format_a_large_number_exceeding_32_bits_correctly_as_a_hexadecimal_string(
        self,
    ):
        assert sprintf("%X", 150460469257) == "2308249009"

    def test_return_0_when_formatting_a_very_small_floating_point_number_as_a_decimal_integer(
        self,
    ):
        assert sprintf("%d", 9.9999e-7) == "0"

    def test_return_0_when_formatting_a_slightly_larger_small_floating_point_number_as_a_decimal_integer(
        self,
    ):
        assert sprintf("%d", 9.9999e-7 + 0.0001) == "0"

    def test_preserve_an_unmatched_named_placeholder_option_is_enabled(self):
        cfg = config().preserve_unmatched_placeholder(True)
        assert cfg.sprintf("%(name)s number 1") == "%(name)s number 1"

    def test_replace_an_unmatched_named_placeholder_with_none_by_default(self):
        assert sprintf("%(name)s number 1") == "none number 1"

    def test_track_named_and_positional_placeholders_correctly(self):
        cfg = config()
        cfg.sprintf("%s %s %s %s %(name)s %1$s %2$s")
        stats = cfg.get_stats()
        assert stats["total_placeholders"] == 7
        assert stats["total_named_placeholder"] == 1
        assert stats["total_positional_placeholder"] == 2
        assert stats["total_sequential_positional_placeholder"] == 4

    def test_track_named_placeholders_correctly(self):
        cfg = config()
        cfg.sprintf("%(firstname)s %(lastname)s")
        stats = cfg.get_stats()
        assert stats["total_placeholders"] == 2
        assert stats["total_named_placeholder"] == 2
        assert stats["total_positional_placeholder"] == 0
        assert stats["total_sequential_positional_placeholder"] == 0

    def test_track_positional_placeholders_correctly(self):
        cfg = config()
        cfg.sprintf("%1$s %2$s")
        stats = cfg.get_stats()
        assert stats["total_placeholders"] == 2
        assert stats["total_named_placeholder"] == 0
        assert stats["total_positional_placeholder"] == 2
        assert stats["total_sequential_positional_placeholder"] == 0

    def test_track_sequential_positional_placeholders_correctly(self):
        cfg = config()
        cfg.sprintf("%s %s")
        stats = cfg.get_stats()
        assert stats["total_placeholders"] == 2
        assert stats["total_named_placeholder"] == 0
        assert stats["total_positional_placeholder"] == 0
        assert stats["total_sequential_positional_placeholder"] == 2


if __name__ == "__main__":
    pytest.main()
