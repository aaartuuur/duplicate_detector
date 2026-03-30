from __future__ import annotations

from pathlib import Path


def ensure_directory(path: Path) -> Path:
    """Проверяет, что путь существует и является папкой."""
    if not path.exists():
        raise ValueError("указанный путь не существует")

    if not path.is_dir():
        raise ValueError("указанный путь не является папкой")

    return path.resolve()
