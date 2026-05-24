from collections import defaultdict

from app.models.file_info import FileInfo
from app.services.hash_service import calculate_file_hash

DuplicateGroups = dict[tuple[str, str], list[FileInfo]]


def find_duplicates(files: list[FileInfo]) -> DuplicateGroups:
    """Находит дубликаты по размеру, расширению и SHA-256."""

    groups_by_size_and_extension: dict[tuple[int, str], list[FileInfo]] = defaultdict(list)

    for file in files:
        key = (file.size, file.extension.lower())
        groups_by_size_and_extension[key].append(file)

    hash_groups: dict[tuple[str, str], list[FileInfo]] = defaultdict(list)

    for group in groups_by_size_and_extension.values():
        if len(group) < 2:
            continue

        for file in group:
            try:
                file_hash = calculate_file_hash(file.path)
                hash_groups[(file_hash, file.extension.lower())].append(file)
            except OSError:
                print(f"Не удалось вычислить хеш: {file.path}")

    return {
        key: group
        for key, group in hash_groups.items()
        if len(group) > 1
    }
