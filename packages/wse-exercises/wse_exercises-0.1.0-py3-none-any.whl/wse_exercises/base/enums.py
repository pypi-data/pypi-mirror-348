"""Defines base class for enumeration."""

from enum import Enum


class BaseEnum(str, Enum):
    """Base class for enumerations."""

    def __str__(self) -> str:
        """Return button text."""
        return self.value
