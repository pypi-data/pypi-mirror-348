"""Defines protocol interfaces for exercises."""

from typing import Protocol

# fmt: off

class IExercises(Protocol):
    """Protocol representing an exercise."""

class IQuestion(Protocol):
    """Protocol representing a task question."""
    @property
    def text(self) -> str: ...

class IAnswer(Protocol):
    """Protocol representing a task answer."""
    @property
    def text(self) -> str: ...

class ITask(Protocol):
    """Protocol representing DTO for all exercise tasks."""
    exercise_type: IExercises
    error_msg: str
    timestamp: float

class IExercise(Protocol):
    """Protocol for exercises with task creation logic."""
    def _get_value(self, key: str, default: int) -> int:
        """Retrieve safely integer value from exercise config."""
    def create_task(self) -> ITask | None:
        """Create a new task DTO with generated conditions."""
    def _create_question(self) -> IQuestion: ...
    def _create_answer(self) -> IAnswer: ...

class IResult(Protocol):
    """Protocol for answer validation results."""
    @property
    def is_correct(self) -> bool: ...
    @property
    def text(self) -> str:
        """Return a string representation of the check result."""
    def __str__(self) -> str:
        """Return the string representation of check result."""
