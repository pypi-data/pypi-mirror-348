"""Defines interfaces for library."""

__all__ = [
    'IExerciseConfig',
    'IOperandGenerator',
    'ISimpleMathAnswer',
    'ISimpleMathExercise',
    'ISimpleMathQuestion',
    'ISimpleMathTask',
]

from wse_exercises.core.mathem.interfaces.iconfig import IExerciseConfig
from wse_exercises.core.mathem.interfaces.iexercise import ISimpleMathExercise
from wse_exercises.core.mathem.interfaces.iservices import IOperandGenerator
from wse_exercises.core.mathem.interfaces.itasks import (
    ISimpleMathAnswer,
    ISimpleMathQuestion,
    ISimpleMathTask,
)
