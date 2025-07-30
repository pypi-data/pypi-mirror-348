"""Defines the base logic for creation a simple math exercise."""

import logging
from abc import ABC
from typing import Type

from wse_exercises.core.mathem.base.task import SimpleMathTask
from wse_exercises.core.mathem.exceptions import OperandGeneratorError
from wse_exercises.core.mathem.interfaces import (
    IOperandGenerator,
    ISimpleMathAnswer,
    ISimpleMathExercise,
    ISimpleMathQuestion,
    ISimpleMathTask,
)
from wse_exercises.core.mathem.interfaces.iconfig import IExerciseConfig
from wse_exercises.interfaces.iexercises import IExercises

logger = logging.getLogger(__name__)

MIN_VALUE = 1
MAX_VALUE = 9


class BaseSimpleCalculationExercise(ABC, ISimpleMathExercise):
    """Defines a base logic of simple calculation exercise creation."""

    _exercise_type: IExercises
    _question_class: Type[ISimpleMathQuestion]
    _answer_class: Type[ISimpleMathAnswer]
    _operand_1: int
    _operand_2: int

    def __init__(
        self,
        operand_generator: IOperandGenerator,
        config: dict | IExerciseConfig | None = None,
    ) -> None:
        """Construct the task creation."""
        if config is not None and not isinstance(
            config, (dict, IExerciseConfig)
        ):
            logger.debug(
                f'Invalid config type: {type(config).__name__}, using empty.'
            )
            config = {}
        self._exercise_config = config or {}

        self._min_value = self._get_value('min_value', MIN_VALUE)
        self._max_value = self._get_value('max_value', MAX_VALUE)
        self._operand_generator = operand_generator
        self._operand_generator.set_values(self._min_value, self._max_value)

    def create_task(self) -> ISimpleMathTask | None:
        """Create new calculation task data transfer object."""
        try:
            self._operand_1 = self._generate_operand()
            self._operand_2 = self._generate_operand()
        except OperandGeneratorError as e:
            logger.exception(str(e))
            return None

        return SimpleMathTask(
            min_value=self._min_value,
            max_value=self._max_value,
            operand_1=self._operand_1,
            operand_2=self._operand_2,
            exercise_type=self._exercise_type,
            question=self._create_question(),
            answer=self._create_answer(),
        )

    # Utility methods

    def _get_value(self, key: str, default: int) -> int:
        value = self._exercise_config.get(key)
        return value if isinstance(value, int) else default

    def _create_question(self) -> ISimpleMathQuestion:
        return self._question_class(self._operand_1, self._operand_2)

    def _create_answer(self) -> ISimpleMathAnswer:
        return self._answer_class(self._operand_1, self._operand_2)

    def _generate_operand(self) -> int:
        """Generate random integer within configured range."""
        return self._operand_generator.generate()
