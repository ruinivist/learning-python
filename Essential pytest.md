# Essential pytest

Install the `pytest` package with pip. Python also includes `unittest`.

## Writing tests

A function and its test are linked by pytest's discovery conventions:

- filenames are either `test_*.py` or `*_test.py`
- function names begin with `test_`
- class names begin with `Test`

Run all tests with `pytest`, or pass a file or directory to run a subset.

### Different types of assertions

- `assert some_bool` is the most common
- for testing raised exceptions you can use `with pytest.raises(MyCustomError):` as a context manager
  and then within that code that raises it. `raises` has args for testing messages etc

### Using fixtures

You write you test function as usual but this time put in args. Let's call the arg variable name
`x`. Then you define a function named `x` and decorate it with `@pytest.fixture`.

- These fixtures are automatically called by pytest, and their return values are passed as args.
- Fixtures are reusable, and one fixture can request another by naming it as an argument.
- Each fixture argument names a fixture.
- Use parametrization to run the same test with multiple sets of values.
- `tmp_path` provides a unique temporary directory for each test.

_teardown_

Yield the fixture value instead of returning it. Put cleanup code after the yield.

### Markers for tagging tests

In `pyproject.toml`, define markers:

```
[tool.pytest.ini_options]
markers = [
    "slow: marks tests as slow",
    "serial",
]
```

Mark a test with `@pytest.mark.slow`, then run `pytest -m slow` or `pytest -m "not slow"`.
Markers label tests; a `serial` marker does not change how pytest runs them by itself.

### Parameterization

use `pytest.mark.parametrize` and supply a string of comma separated names then array with
tuples of args.

```python
@pytest.mark.parametrize("number, expected", [(2, 4), (3, 6), (9, 18)])
def test_double(number, expected):
    assert number * 2 == expected
```

### Mocking

This uses python's monkeypatching.
You make the mock function, name doesn't matter.

Then do `monkeypatch.setattr(Path, "home", mockpath)` inside the test.
This will change behavior of `Path.home` func from python's pathlib.

### Grouping tests

Equivalent of a test group or describe block from other languages.

Both class and function names should follow the convention; this allows pytest
to differentiate non test members of the class.

```python
class TestUser:
    @pytest.fixture
    def user(self):
        return {"name": "Alice", "active": True}

    def test_has_name(self, user):
        assert user["name"] == "Alice"

    def test_is_active(self, user):
        assert user["active"] is True
```

## Examples

Run them with `cd pytest-examples && uv run pytest`.

- [`test_basics.py`](pytest-examples/test_basics.py): assertions, `pytest.raises` with a message match, and parametrization.
- [`test_fixtures.py`](pytest-examples/test_fixtures.py): reusable and dependent fixtures, `tmp_path`, yield teardown, and tests grouped in `TestUser`.
- [`markers_test.py`](pytest-examples/markers_test.py): the `*_test.py` filename convention and `slow` and `serial` markers.
- [`test_mocks.py`](pytest-examples/test_mocks.py): replacing `Path.home` with `monkeypatch`.
- [`pyproject.toml`](pytest-examples/pyproject.toml): marker registration; try `uv run pytest -m slow` and `uv run pytest -m "not slow"` from `pytest-examples`.
