import pytest


def test_truthy_assertion():
    assert "pytest".startswith("py")


def test_raises_value_error():
    with pytest.raises(ValueError, match="invalid literal"):
        int("not a number")


@pytest.mark.parametrize("number, expected", [(2, 4), (3, 6), (9, 18)])
def test_double(number, expected):
    assert number * 2 == expected
