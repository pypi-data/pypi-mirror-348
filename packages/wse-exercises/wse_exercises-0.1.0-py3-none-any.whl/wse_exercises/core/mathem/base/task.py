"""Defines the base logic for creation a simple math task and answer."""

import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from wse_exercises.core.mathem.interfaces.itasks import (
    ISimpleMathAnswer,
    ISimpleMathQuestion,
    ISimpleMathTask,
)
from wse_exercises.interfaces.iexercises import IExercises


@dataclass(frozen=True)
class SimpleMathTask(ISimpleMathTask):
    """Mathematical task DTO."""

    min_value: int
    max_value: int
    operand_1: int
    operand_2: int
    question: ISimpleMathQuestion
    answer: ISimpleMathAnswer
    exercise_type: IExercises
    error_msg: str = ''
    timestamp: float = field(default_factory=time.time)


class SimpleMathTaskComponent(ABC):
    """Defines the logic for creating a simple math task or answer."""

    def __init__(self, operand_1: int, operand_2: int) -> None:
        """Construct the logic creation."""
        self._operand_1 = operand_1
        self._operand_2 = operand_2
        self._create()

    @abstractmethod
    def _create(self) -> None:
        """Create a simple math task or answer."""


class TextQuestionMixin:
    """Mixin for string representation of the task question."""

    _question: str

    @property
    def text(self) -> str:
        """Return a string representation of the task question."""
        return self._question


class TextAnswerMixin:
    """Mixin for string representation of the task answer."""

    _answer: int

    @property
    def text(self) -> str:
        """Return a string representation of the task answer."""
        return str(self._answer)


class SimpleTextQuestion(TextQuestionMixin, SimpleMathTaskComponent, ABC):
    """Combines simple task question creation and its property."""


class SimpleTextAnswer(TextAnswerMixin, SimpleMathTaskComponent, ABC):
    """Combines simple task answer creation and its property."""
