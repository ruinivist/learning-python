import pytest


@pytest.fixture
def user():
    return {"name": "Alice", "active": True}


@pytest.fixture
def greeting(user):
    return f"Hello, {user['name']}"


@pytest.fixture
def temp_file(tmp_path):
    path = tmp_path / "example.txt"
    path.write_text("ready")
    yield path
    path.unlink()


def test_fixture_can_use_another(greeting):
    assert greeting == "Hello, Alice"


def test_tmp_path(tmp_path):
    path = tmp_path / "message.txt"
    path.write_text("hello")
    assert path.read_text() == "hello"


def test_yield_fixture(temp_file):
    assert temp_file.read_text() == "ready"


class TestUser:
    def test_has_name(self, user):
        assert user["name"] == "Alice"

    def test_is_active(self, user):
        assert user["active"] is True
