"""Defines math exercise config."""

from dataclasses import dataclass

from wse_exercises.core.mathem.base.exercise_config import BaseExerciseConfig


@dataclass
class ExerciseConfig(BaseExerciseConfig):
    """Exercise config Data-Transfer-Object."""

    min_value: int
    max_value: int
