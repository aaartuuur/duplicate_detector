from duplicate_detector.app.main import main


def test_main_without_arguments_shows_usage(capsys):
    exit_code = main([])

    output = capsys.readouterr().out

    assert exit_code == 0
    assert "Использование" in output


def test_main_with_missing_directory_returns_error(tmp_path, capsys):
    exit_code = main([str(tmp_path / "missing")])

    output = capsys.readouterr().out

    assert exit_code == 1
    assert "Ошибка: папка не найдена" in output


def test_main_with_no_duplicates(tmp_path, capsys):
    (tmp_path / "a.txt").write_text("hello", encoding="utf-8")
    (tmp_path / "b.txt").write_text("world", encoding="utf-8")

    exit_code = main([str(tmp_path)])

    output = capsys.readouterr().out

    assert exit_code == 0
    assert "Дубликаты не найдены" in output


def test_main_with_duplicates_and_cancel_deletion(tmp_path, monkeypatch, capsys):
    file1 = tmp_path / "a.txt"
    file2 = tmp_path / "b.txt"
    file1.write_text("same", encoding="utf-8")
    file2.write_text("same", encoding="utf-8")

    monkeypatch.setattr("builtins.input", lambda _: "n")

    exit_code = main([str(tmp_path)])

    output = capsys.readouterr().out

    assert exit_code == 0
    assert "Найдено групп дубликатов" in output
    assert "Удаление отменено" in output
    assert file1.exists()
    assert file2.exists()


def test_main_with_duplicates_and_confirm_deletion(tmp_path, monkeypatch, capsys):
    file1 = tmp_path / "a.txt"
    file2 = tmp_path / "b.txt"
    file1.write_text("same", encoding="utf-8")
    file2.write_text("same", encoding="utf-8")
    answers = iter(["y", "1", "y"])

    monkeypatch.setattr("builtins.input", lambda _: next(answers))

    exit_code = main([str(tmp_path)])

    output = capsys.readouterr().out

    assert exit_code == 0
    assert "Удалено файлов: 1" in output
    assert file1.exists()
    assert not file2.exists()
