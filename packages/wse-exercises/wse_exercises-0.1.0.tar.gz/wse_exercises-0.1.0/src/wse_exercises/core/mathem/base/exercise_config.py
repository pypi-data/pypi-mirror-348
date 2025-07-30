"""Defines math base exercise config."""

from abc import ABC

from wse_exercises.core.mathem.interfaces import IExerciseConfig


class BaseExerciseConfig(ABC, IExerciseConfig):
    """Base exercise config DTO."""

    min_value: int
    max_value: int

    def get(self, key: str, default: int | None = None) -> int | None:
        """Get value by key."""
        return getattr(self, key, default)

    def __getitem__(self, key: str) -> int:
        """Get value by ['key']."""
        if not hasattr(self, key):
            raise KeyError(f'Key "{key}" not found in exercise config')
        return getattr(self, key)
