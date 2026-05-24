from duplicate_detector.app.services.file_scanner import scan_files


def test_scan_files_finds_files_recursively(tmp_path):
    nested = tmp_path / "nested"
    nested.mkdir()
    file1 = tmp_path / "a.txt"
    file2 = nested / "b.log"

    file1.write_text("a", encoding="utf-8")
    file2.write_text("bb", encoding="utf-8")

    files = scan_files(tmp_path)

    assert {file.name for file in files} == {"a.txt", "b.log"}
    assert {file.extension for file in files} == {".txt", ".log"}


def test_scan_files_can_scan_only_top_level(tmp_path):
    nested = tmp_path / "nested"
    nested.mkdir()
    file1 = tmp_path / "a.txt"
    file2 = nested / "b.txt"

    file1.write_text("a", encoding="utf-8")
    file2.write_text("b", encoding="utf-8")

    files = scan_files(tmp_path, recursive=False)

    assert [file.name for file in files] == ["a.txt"]
