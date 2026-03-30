from __future__ import annotations

from pathlib import Path

from app.models.file_info import FileInfo


class FileScanner:
    """Сервис для обхода папки и сбора информации о файлах."""

    def scan(self, directory: Path) -> list[FileInfo]:
        files: list[FileInfo] = []

        for item in directory.rglob("*"):
            if item.is_file():
                files.append(self._build_file_info(item))

        return files

    def _build_file_info(self, file_path: Path) -> FileInfo:
        return FileInfo(
            path=file_path.resolve(),
            name=file_path.name,
            size=file_path.stat().st_size,
            extension=file_path.suffix.lower(),
        )
