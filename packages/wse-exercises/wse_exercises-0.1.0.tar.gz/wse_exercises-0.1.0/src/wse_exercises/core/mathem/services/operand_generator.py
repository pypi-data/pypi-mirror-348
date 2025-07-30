"""Defines generation math exercises operands."""

from random import randint

from wse_exercises.core.mathem.base.servises import BaseOperandGenerator
from wse_exercises.core.mathem.exceptions import OperandGeneratorError
from wse_exercises.utils.logger import setup_logging

logger = setup_logging(__name__)


class RandomOperandGenerator(BaseOperandGenerator):
    """Random generator of integer operands within configured range."""

    def generate(self) -> int:
        """Generate random integer within configured range."""
        return randint(self._min_value, self._max_value)


class ExactOperandGenerator(BaseOperandGenerator):
    """Return value by order."""

    def __init__(self) -> None:
        """Construct the generator."""
        self._index = 0
        self._values: list[int] = []

    def set_values(self, min_value: int, max_value: int) -> None:
        """Set values for operand generation."""
        self._values.append(min_value)
        self._values.append(max_value)

    def generate(self) -> int:
        """Return value by order."""
        try:
            value = self._values[self._index]
        except IndexError as error:
            raise OperandGeneratorError from error
        self._index += 1
        return value
