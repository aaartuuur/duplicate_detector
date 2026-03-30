from __future__ import annotations

import sys
from pathlib import Path

from app.services.file_scanner import FileScanner
from app.utils.path_utils import ensure_directory


def get_directory_from_user() -> Path:
    """Получает путь к папке из аргумента командной строки или через input."""
    if len(sys.argv) > 1:
        return Path(sys.argv[1])

    raw_path = input("Введите путь к папке для сканирования: ").strip()
    return Path(raw_path)


def main() -> None:
    directory = get_directory_from_user()

    try:
        directory = ensure_directory(directory)
    except ValueError as error:
        print(f"Ошибка: {error}")
        return

    scanner = FileScanner()
    files = scanner.scan(directory)

    print(f"\nНайдено файлов: {len(files)}")
    print("-" * 60)

    for file_info in files:
        print(f"Имя: {file_info.name}")
        print(f"Путь: {file_info.path}")
        print(f"Размер: {file_info.size} байт")
        print(f"Расширение: {file_info.extension or 'без расширения'}")
        print("-" * 60)


if __name__ == "__main__":
    main()
