from duplicate_detector.app.services.hash_service import calculate_file_hash


def test_same_files_have_same_hash(tmp_path):
    file1 = tmp_path / "a.txt"
    file2 = tmp_path / "b.txt"

    file1.write_text("hello", encoding="utf-8")
    file2.write_text("hello", encoding="utf-8")

    assert calculate_file_hash(file1) == calculate_file_hash(file2)


def test_different_files_have_different_hashes(tmp_path):
    file1 = tmp_path / "a.txt"
    file2 = tmp_path / "b.txt"

    file1.write_text("hello", encoding="utf-8")
    file2.write_text("world", encoding="utf-8")

    assert calculate_file_hash(file1) != calculate_file_hash(file2)


def test_hash_is_stable_for_small_chunk_size(tmp_path):
    file_path = tmp_path / "data.bin"
    file_path.write_bytes(b"abcdef" * 100)

    assert calculate_file_hash(file_path, chunk_size=3) == calculate_file_hash(file_path)
