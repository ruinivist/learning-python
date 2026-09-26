from pathlib import Path


def test_monkeypatch(monkeypatch, tmp_path):
    def fake_home():
        return tmp_path

    monkeypatch.setattr(Path, "home", fake_home)
    assert Path.home() == tmp_path
