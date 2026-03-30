from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class FileInfo:
    """Модель с базовой информацией о файле."""

    path: Path
    name: str
    size: int
    extension: str
