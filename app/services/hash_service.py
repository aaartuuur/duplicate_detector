import hashlib
from pathlib import Path


def calculate_file_hash(file_path: Path, chunk_size: int = 65536) -> str:
    hasher = hashlib.sha256()

    with file_path.open("rb") as file:
        while chunk := file.read(chunk_size):
            hasher.update(chunk)

    return hasher.hexdigest()