from pathlib import Path
from typing import List

from app.models.file_info import FileInfo


def scan_files(folder: Path) -> List[FileInfo]:
    files: List[FileInfo] = []

    for item in folder.rglob("*"):
        if item.is_file():
            try:
                files.append(
                    FileInfo(
                        path=item.resolve(),
                        name=item.name,
                        size=item.stat().st_size,
                        extension=item.suffix.lower()
                    )
                )
            except OSError:
                print(f"Не удалось прочитать файл: {item}")

    return files