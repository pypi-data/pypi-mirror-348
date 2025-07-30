"""Defines protocols for math exercises services."""

from typing import Callable, Protocol

from wse_exercises.core.mathem.interfaces import ISimpleMathExercise
from wse_exercises.interfaces import IExercises

# fmt: off


class IOperandGenerator(Protocol):
    """Protocol for generator of integer operands."""
    def set_values(self, min_value: int, max_value: int) -> None:
        """Set value range for operands generate."""
    def generate(self) -> int:
        """Generate integer within configured range."""


class IExerciseSwitcher(Protocol):
    """Exercise provider switcher."""
    def switch(self, exercise_name: str) -> None:
        """Set current exercise type."""
    @property
    def current_exercise_name(self) -> IExercises: ...
    @property
    def current_exercise(self) -> ISimpleMathExercise: ...
    @property
    def exercises(self) -> dict[IExercises, Callable]: ...
