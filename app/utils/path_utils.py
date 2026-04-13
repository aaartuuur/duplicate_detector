from pathlib import Path


def validate_directory(path: Path) -> bool:
    return path.exists() and path.is_dir()