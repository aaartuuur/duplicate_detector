from dataclasses import dataclass
from pathlib import Path


@dataclass
class FileInfo:
    path: Path
    name: str
    size: int
    extension: str