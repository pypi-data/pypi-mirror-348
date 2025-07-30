"""Defines protocols for exercise configuration data."""

from typing import Protocol, runtime_checkable


@runtime_checkable
class IExerciseConfig(Protocol):
    """Protocol for exercise config Data Transfer Object."""

    def get(self, key: str, default: int | None = None) -> int | None: ...
    def __getitem__(self, key: str) -> int:
        """Get value by ['key']."""
