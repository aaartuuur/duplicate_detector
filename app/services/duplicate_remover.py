from collections.abc import Sequence

from duplicate_detector.app.models.deletion_summary import DeletionSummary
from duplicate_detector.app.models.file_info import FileInfo
from duplicate_detector.app.services.duplicate_finder import DuplicateGroups


def delete_all_except(group: Sequence[FileInfo], keep_file: FileInfo) -> DeletionSummary:

    deleted_files_count = 0
    freed_bytes = 0

    for file in group:
        if file.path == keep_file.path:
            continue

        file.path.unlink()
        deleted_files_count += 1
        freed_bytes += file.size

    return DeletionSummary(deleted_files_count, freed_bytes)


def remove_duplicates(duplicates: DuplicateGroups) -> DeletionSummary:

    total_summary = DeletionSummary()

    for group_index, ((file_hash, extension), group) in enumerate(duplicates.items(), start=1):
        print(f"\nГруппа {group_index}")
        extension_text = extension if extension else '[без расширения]'
        print(f"Расширение: {extension_text}")
        print(f"Хеш: {file_hash}")
        print("Файлы:")

        for index, file in enumerate(group, start=1):
            print(f"{index}. {file.name} | {file.size} bytes")
            print(f"   {file.path}")

        keep_index = _ask_keep_index(len(group))

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

        try:
            summary = delete_all_except(group, keep_file)
            total_summary += summary
            _print_deleted_files(group, keep_file)
        except OSError as error:
            print(f"Ошибка при удалении файлов: {error}")

    print("\nУдаление завершено.")
    print(f"Удалено файлов: {total_summary.deleted_files_count}")
    print(f"Освобождено байт: {total_summary.freed_bytes}")

    return total_summary


def _ask_keep_index(group_length: int) -> int:
    while True:
        user_input = input(
            "\nВведите номер файла, который нужно оставить "
            "(или 0, чтобы пропустить группу): "
        ).strip()

        if not user_input.isdigit():
            print("Ошибка: введите число.")
            continue

        keep_index = int(user_input)

        if 0 <= keep_index <= group_length:
            return keep_index

        print("Ошибка: такого номера нет.")


def _print_deleted_files(group: Sequence[FileInfo], keep_file: FileInfo) -> None:
    for file in group:
        if file.path != keep_file.path:
            print(f"Удалён: {file.path}")
