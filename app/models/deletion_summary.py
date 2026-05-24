from dataclasses import dataclass


@dataclass(frozen=True)
class DeletionSummary:
    """Результат удаления файлов."""

    deleted_files_count: int = 0
    freed_bytes: int = 0

    def __add__(self, other: "DeletionSummary") -> "DeletionSummary":
        return DeletionSummary(
            deleted_files_count=self.deleted_files_count + other.deleted_files_count,
            freed_bytes=self.freed_bytes + other.freed_bytes,
        )
