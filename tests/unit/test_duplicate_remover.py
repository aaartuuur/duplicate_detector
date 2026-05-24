from duplicate_detector.app.models.file_info import FileInfo
from duplicate_detector.app.services.duplicate_remover import delete_all_except, remove_duplicates
from duplicate_detector.app.services.hash_service import calculate_file_hash


def make_file_info(path):
    return FileInfo(
        path=path,
        name=path.name,
        size=path.stat().st_size,
        extension=path.suffix.lower(),
    )


def test_delete_all_except_keeps_selected_file_and_deletes_others(tmp_path):
    keep = tmp_path / "keep.txt"
    duplicate = tmp_path / "duplicate.txt"

    keep.write_text("same", encoding="utf-8")
    duplicate.write_text("same", encoding="utf-8")

    keep_info = make_file_info(keep)
    duplicate_info = make_file_info(duplicate)

    summary = delete_all_except([keep_info, duplicate_info], keep_info)

    assert keep.exists()
    assert not duplicate.exists()
    assert summary.deleted_files_count == 1
    assert summary.freed_bytes == duplicate_info.size


def test_remove_duplicates_can_skip_group(tmp_path, monkeypatch):
    file1 = tmp_path / "a.txt"
    file2 = tmp_path / "b.txt"
    file1.write_text("same", encoding="utf-8")
    file2.write_text("same", encoding="utf-8")

    file1_info = make_file_info(file1)
    file2_info = make_file_info(file2)
    duplicates = {(calculate_file_hash(file1), ".txt"): [file1_info, file2_info]}

    monkeypatch.setattr("builtins.input", lambda _: "0")

    summary = remove_duplicates(duplicates)

    assert file1.exists()
    assert file2.exists()
    assert summary.deleted_files_count == 0


def test_remove_duplicates_deletes_after_confirmation(tmp_path, monkeypatch):
    file1 = tmp_path / "a.txt"
    file2 = tmp_path / "b.txt"
    file1.write_text("same", encoding="utf-8")
    file2.write_text("same", encoding="utf-8")

    file1_info = make_file_info(file1)
    file2_info = make_file_info(file2)
    duplicates = {(calculate_file_hash(file1), ".txt"): [file1_info, file2_info]}
    answers = iter(["1", "y"])

    monkeypatch.setattr("builtins.input", lambda _: next(answers))

    summary = remove_duplicates(duplicates)

    assert file1.exists()
    assert not file2.exists()
    assert summary.deleted_files_count == 1
