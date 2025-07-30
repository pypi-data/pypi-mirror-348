"""Defines abstract base classes for services."""

from abc import ABC, abstractmethod

from wse_exercises.core.mathem.interfaces.iservices import IOperandGenerator


class BaseOperandGenerator(ABC, IOperandGenerator):
    """Base generator of integer operands within configured range."""

    _min_value: int
    _max_value: int

    def set_values(self, min_value: int, max_value: int) -> None:
        """Set operand value range."""
        self._min_value = min_value
        self._max_value = max_value

    @abstractmethod
    def generate(self) -> int:
        """Generate integer within configured range."""
