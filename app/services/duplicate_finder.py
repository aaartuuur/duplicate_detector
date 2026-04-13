from collections import defaultdict
from typing import Dict, List, Tuple

from app.models.file_info import FileInfo
from app.services.hash_service import calculate_file_hash


def find_duplicates(files: List[FileInfo]) -> Dict[Tuple[str, str], List[FileInfo]]:
    groups_by_size_and_extension = defaultdict(list)

    for file in files:
        key = (file.size, file.extension.lower())
        groups_by_size_and_extension[key].append(file)

    hash_groups = defaultdict(list)

    for group in groups_by_size_and_extension.values():
        if len(group) < 2:
            continue

        for file in group:
            try:
                file_hash = calculate_file_hash(file.path)
                hash_groups[(file_hash, file.extension.lower())].append(file)
            except OSError:
                print(f"Не удалось вычислить хеш: {file.path}")

    duplicates = {
        key: group
        for key, group in hash_groups.items()
        if len(group) > 1
    }

    return duplicates