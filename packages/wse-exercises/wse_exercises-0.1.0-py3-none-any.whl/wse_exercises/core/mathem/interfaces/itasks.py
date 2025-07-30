"""Defines protocols for simple math exercise task and answer."""

from typing import Protocol

from wse_exercises.interfaces.iexercises import (
    IAnswer,
    IQuestion,
    ITask,
)

# fmt: off

class ISimpleMathQuestion(IQuestion, Protocol):
    """Protocol representing a task question."""
    _operand_1: int
    _operand_2: int
    def __init__(self, operand_1: int, operand_2: int) -> None: ...  # noqa: D107

class ISimpleMathAnswer(IAnswer, Protocol):
    """Protocol representing a task answer."""
    _operand_1: int
    _operand_2: int
    def __init__(self, operand_1: int, operand_2: int) -> None: ...  # noqa: D107

class ISimpleMathTask(ITask, Protocol):
    """Adds math-specific constraints to ITask."""
    min_value: int
    max_value: int
    operand_1: int
    operand_2: int
    question: ISimpleMathQuestion
    answer: ISimpleMathAnswer
