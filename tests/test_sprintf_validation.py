import pytest
from pyprintf import sprintf, config


class TestCallback:
    def test_throw_error_when_we_try_to_format_a_string_using_lambda(self):
        with pytest.raises(ValueError) as exc:
            sprintf("%s", lambda: "foobar")

    def test_not_throw_error_when_we_try_to_format_undefined_as_undefined_using_lambda(
        self,
    ):
        try:
            sprintf("%T", None)
        except TypeError:
            pytest.fail(f"TypeError")


class TestInvalidPlaceholders:
    def test_throw_valueerror_for_missing_parameter(self):
        with pytest.raises(ValueError) as exc:
            cfg = config().throw_error_on_unmatched(True)
            cfg.sprintf("Two params needed 1: %s 2: %s", "one")

    def test_throw_valueerror_for_missing_arguments_by_index(self):
        with pytest.raises(ValueError) as exc:
            cfg = config().throw_error_on_unmatched(True)
            cfg.sprintf("%2$s %3$s a %1$s", "cracker", "Polly")

    def test_throw_valueerror_for_missing_arguments_by_name(self):
        with pytest.raises(ValueError) as exc:
            cfg = config().throw_error_on_unmatched(True)
            cfg.sprintf(
                "Two params needed 1: %(first)s 2: %(second)s", {"first": "one"}
            )

    def test_throw_syntaxerror_for_a_single_percent_sign(self):
        with pytest.raises(SyntaxError) as exc:
            cfg = config().throw_error_on_unmatched(True)
            cfg.sprintf("%")

    def test_throw_syntaxerror_for_a_percent_sign_followed_by_an_invalid_character(
        self,
    ):
        with pytest.raises(SyntaxError) as exc:
            cfg = config().throw_error_on_unmatched(True)
            cfg.sprintf("%A")

    def test_throw_syntaxerror_for_a_percent_sign_within_a_string_placeholder(self):
        with pytest.raises(SyntaxError) as exc:
            cfg = config().throw_error_on_unmatched(True)
            cfg.sprintf("%s%")

    def test_throw_syntaxerror_for_an_unclosed_named_placeholder_opening_parenthesis(
        self,
    ):
        with pytest.raises(SyntaxError) as exc:
            cfg = config().throw_error_on_unmatched(True)
            cfg.sprintf("%(s")

    def test_throw_syntaxerror_for_an_unclosed_named_placeholder_closing_parenthesis(
        self,
    ):
        with pytest.raises(SyntaxError) as exc:
            cfg = config().throw_error_on_unmatched(True)
            cfg.sprintf("%)s")

    def test_throw_syntaxerror_for_an_empty_named_placeholder(self):
        with pytest.raises(SyntaxError) as exc:
            cfg = config().throw_error_on_unmatched(True)
            cfg.sprintf("%()s")

    def test_throw_syntaxerror_for_a_named_placeholder_with_a_numeric_name(self):
        with pytest.raises(SyntaxError) as exc:
            cfg = config().throw_error_on_unmatched(True)
            cfg.sprintf("%(12)s")


def assert_raises_type_error(fmt, *args):
    with pytest.raises(TypeError):
        sprintf(fmt, *args)


def assert_does_not_raise_type_error(fmt, *args):
    try:
        sprintf(fmt, *args)
    except TypeError:
        pytest.fail(f"TypeError was raised for {fmt} with arguments {args}")


class TestInvalidArgumentsForNumericSpecifiers:
    numeric_specifiers = list("bcdiefguxX")

    @pytest.mark.parametrize("specifier", numeric_specifiers)
    def test_valid_implicit_casts_no_type_error(self, specifier):
        fmt = sprintf("%%%s", specifier)
        assert_does_not_raise_type_error(fmt, [True])
        assert_does_not_raise_type_error(fmt, [1])
        assert_does_not_raise_type_error(fmt, ["200"])
        assert_does_not_raise_type_error(fmt, [None])


class TestNamedPlaceholdersWithObjectAccess:
    def test_not_throw_an_error_when_accessing_a_property_that_evaluates_to_none(self):
        with pytest.raises(ValueError) as exc:
            cfg = config().throw_error_on_unmatched(True)
            cfg.sprintf("%(x.y)s", {"x": {}})

    def test_throw_an_error_containing_sprintf_when_accessing_a_property_that_would_raise_typeerror(
        self,
    ):
        with pytest.raises(ValueError) as exc:
            cfg = config().throw_error_on_unmatched(True)
            cfg.sprintf("%(x.y)s", {})


if __name__ == "__main__":
    pytest.main()
