import os
import subprocess
import sys


def run_cli(project_root, *args, input_text=""):
    env = os.environ.copy()
    env["PYTHONPATH"] = str(project_root)

    return subprocess.run(
        [sys.executable, "-m", "app.main", *map(str, args)],
        input=input_text,
        text=True,
        capture_output=True,
        cwd=project_root,
        env=env,
        check=False,
    )


def test_cli_without_arguments_shows_usage(project_root):
    result = run_cli(project_root)

    assert result.returncode == 0
    assert "Использование" in result.stdout


def test_cli_with_missing_directory_shows_error(project_root, tmp_path):
    result = run_cli(project_root, tmp_path / "missing")

    assert result.returncode == 1
    assert "Ошибка: папка не найдена" in result.stdout


def test_cli_no_duplicates(project_root, tmp_path):
    (tmp_path / "a.txt").write_text("hello", encoding="utf-8")
    (tmp_path / "b.txt").write_text("world", encoding="utf-8")

    result = run_cli(project_root, tmp_path)

    assert result.returncode == 0
    assert "Дубликаты не найдены" in result.stdout


def test_cli_finds_duplicates_and_user_cancels_deletion(project_root, tmp_path):
    file1 = tmp_path / "a.txt"
    file2 = tmp_path / "b.txt"
    file1.write_text("same", encoding="utf-8")
    file2.write_text("same", encoding="utf-8")

    result = run_cli(project_root, tmp_path, input_text="n\n")

    assert result.returncode == 0
    assert "Найдено групп дубликатов" in result.stdout
    assert "Удаление отменено" in result.stdout
    assert file1.exists()
    assert file2.exists()


def test_cli_deletes_duplicate_after_user_confirmation(project_root, tmp_path):
    file1 = tmp_path / "a.txt"
    file2 = tmp_path / "b.txt"
    file1.write_text("same", encoding="utf-8")
    file2.write_text("same", encoding="utf-8")

    result = run_cli(project_root, tmp_path, input_text="y\n1\ny\n")

    assert result.returncode == 0
    assert "Удалено файлов: 1" in result.stdout
    assert file1.exists()
    assert not file2.exists()
