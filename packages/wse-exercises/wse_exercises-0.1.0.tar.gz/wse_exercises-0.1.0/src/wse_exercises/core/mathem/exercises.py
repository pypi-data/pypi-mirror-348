"""Defines mathematical exercises."""

from wse_exercises.core.mathem.base.exercise import (
    BaseSimpleCalculationExercise,
)
from wse_exercises.core.mathem.calculation_components import (
    AddAnswer,
    AddQuestion,
    DivAnswer,
    DivQuestion,
    MulAnswer,
    MulQuestion,
    SubAnswer,
    SubQuestion,
)
from wse_exercises.core.mathem.enums import Exercises


class AddingExercise(BaseSimpleCalculationExercise):
    """Adding exercise."""

    _exercise_type = Exercises.ADDING
    _question_class = AddQuestion
    _answer_class = AddAnswer


class DivisionExercise(BaseSimpleCalculationExercise):
    """Division exercise."""

    _exercise_type = Exercises.DIVISION
    _question_class = DivQuestion
    _answer_class = DivAnswer


class MultiplicationExercise(BaseSimpleCalculationExercise):
    """Multiplication exercise."""

    _exercise_type = Exercises.MULTIPLICATION
    _question_class = MulQuestion
    _answer_class = MulAnswer


class SubtractionExercise(BaseSimpleCalculationExercise):
    """Subtraction exercise."""

    _exercise_type = Exercises.SUBTRACTION
    _question_class = SubQuestion
    _answer_class = SubAnswer
