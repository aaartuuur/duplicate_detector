from duplicate_detector.app.models.file_info import FileInfo
from duplicate_detector.app.services.duplicate_finder import find_duplicates


def make_file_info(path):
    return FileInfo(
        path=path,
        name=path.name,
        size=path.stat().st_size,
        extension=path.suffix.lower(),
    )


def test_find_duplicates_detects_equal_files(tmp_path):
    file1 = tmp_path / "a.txt"
    file2 = tmp_path / "b.txt"
    file3 = tmp_path / "c.txt"

    file1.write_text("same", encoding="utf-8")
    file2.write_text("same", encoding="utf-8")
    file3.write_text("different", encoding="utf-8")

    duplicates = find_duplicates(
        [make_file_info(file1), make_file_info(file2), make_file_info(file3)]
    )

    assert len(duplicates) == 1
    group = next(iter(duplicates.values()))
    assert {file.name for file in group} == {"a.txt", "b.txt"}


def test_find_duplicates_does_not_mix_extensions(tmp_path):
    txt_file = tmp_path / "a.txt"
    md_file = tmp_path / "a.md"

    txt_file.write_text("same", encoding="utf-8")
    md_file.write_text("same", encoding="utf-8")

    duplicates = find_duplicates([make_file_info(txt_file), make_file_info(md_file)])

    assert duplicates == {}


def test_find_duplicates_ignores_unique_files(tmp_path):
    file1 = tmp_path / "a.txt"
    file2 = tmp_path / "b.txt"

    file1.write_text("one", encoding="utf-8")
    file2.write_text("two", encoding="utf-8")

    duplicates = find_duplicates([make_file_info(file1), make_file_info(file2)])

    assert duplicates == {}
