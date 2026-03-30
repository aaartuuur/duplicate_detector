from pathlib import Path

from app.services.file_scanner import FileScanner


def test_scanner_finds_files(tmp_path: Path) -> None:
    (tmp_path / "a.txt").write_text("hello", encoding="utf-8")
    nested_dir = tmp_path / "nested"
    nested_dir.mkdir()
    (nested_dir / "b.txt").write_text("world", encoding="utf-8")

    scanner = FileScanner()
    files = scanner.scan(tmp_path)

    names = sorted(file.name for file in files)
    assert names == ["a.txt", "b.txt"]
