from duplicate_detector.app.utils.path_utils import validate_directory


def test_validate_directory_returns_true_for_existing_directory(tmp_path):
    assert validate_directory(tmp_path) is True


def test_validate_directory_returns_false_for_file(tmp_path):
    file_path = tmp_path / "file.txt"
    file_path.write_text("content", encoding="utf-8")

    assert validate_directory(file_path) is False


def test_validate_directory_returns_false_for_missing_path(tmp_path):
    assert validate_directory(tmp_path / "missing") is False
