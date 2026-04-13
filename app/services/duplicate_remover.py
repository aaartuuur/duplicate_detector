from typing import Dict, List, Tuple

from app.models.file_info import FileInfo


def remove_duplicates(duplicates: Dict[Tuple[str, str], List[FileInfo]]) -> None:
    deleted_files_count = 0
    freed_bytes = 0

    for group_index, ((file_hash, extension), group) in enumerate(duplicates.items(), start=1):
        print(f"\nГруппа {group_index}")
        print(f"Расширение: {extension if extension else '[без расширения]'}")
        print(f"Хеш: {file_hash}")
        print("Файлы:")

        for index, file in enumerate(group, start=1):
            print(f"{index}. {file.name} | {file.size} bytes")
            print(f"   {file.path}")

        while True:
            user_input = input(
                "\nВведите номер файла, который нужно оставить "
                "(или 0, чтобы пропустить группу): "
            ).strip()

            if not user_input.isdigit():
                print("Ошибка: введите число.")
                continue

            keep_index = int(user_input)

            if 0 <= keep_index <= len(group):
                break

            print("Ошибка: такого номера нет.")

        if keep_index == 0:
            print("Группа пропущена.")
            continue

        keep_file = group[keep_index - 1]

        confirm = input(
            f'Оставить "{keep_file.name}" и удалить остальные? (y/n): '
        ).strip().lower()

        if confirm != "y":
            print("Удаление отменено для этой группы.")
            continue

        for file in group:
            if file.path == keep_file.path:
                continue

            try:
                file.path.unlink()
                deleted_files_count += 1
                freed_bytes += file.size
                print(f"Удалён: {file.path}")
            except OSError as error:
                print(f"Не удалось удалить {file.path}: {error}")

    print("\nУдаление завершено.")
    print(f"Удалено файлов: {deleted_files_count}")
    print(f"Освобождено байт: {freed_bytes}")