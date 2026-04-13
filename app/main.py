import sys
from pathlib import Path

from app.services.duplicate_finder import find_duplicates
from app.services.file_scanner import scan_files
from app.utils.path_utils import validate_directory


def main() -> None:
    if len(sys.argv) < 2:
        print("Использование:")
        print(r'python -m app.main "C:\путь\к\папке"')
        return

    folder = Path(sys.argv[1])

    if not validate_directory(folder):
        print(f"Ошибка: папка не найдена -> {folder}")
        return

    print(f"Сканирование папки: {folder}")
    files = scan_files(folder)
    print(f"Всего найдено файлов: {len(files)}")

    duplicates = find_duplicates(files)

    if not duplicates:
        print("\nДубликаты не найдены.")
        return

    print(f"\nНайдено групп дубликатов: {len(duplicates)}\n")

    for group_index, ((file_hash, extension), group) in enumerate(duplicates.items(), start=1):
        print(f"Группа {group_index}")
        print(f"Расширение: {extension if extension else '[без расширения]'}")
        print(f"Хеш: {file_hash}")
        print(f"Количество файлов: {len(group)}")

        for file in group:
            print(f" - {file.name} | {file.size} bytes")
            print(f"   {file.path}")

        print()


if __name__ == "__main__":
    main()