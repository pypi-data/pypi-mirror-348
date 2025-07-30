"""Defines protocols for simple math exercise task and answer."""

from typing import Protocol

from wse_exercises.interfaces import IExercise

# fmt: off


class ISimpleMathExercise(IExercise, Protocol):
    """Defines a task creation logic of simple calculation exercise."""
    def _generate_operand(self) -> int: ...
