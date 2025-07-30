"""Defines the calculation exercise components."""

from wse_exercises.core.mathem.base.task import (
    SimpleTextAnswer,
    SimpleTextQuestion,
)


class AddQuestion(SimpleTextQuestion):
    """A multiplication task question."""

    def _create(self) -> None:
        self._question = f'{self._operand_1} + {self._operand_2}'


class AddAnswer(SimpleTextAnswer):
    """A multiplication task answer."""

    def _create(self) -> None:
        self._answer = self._operand_1 + self._operand_2


class DivQuestion(SimpleTextQuestion):
    """A division task question."""

    def _create(self) -> None:
        self._question = (
            f'{self._operand_1 * self._operand_2} : {self._operand_2}'
        )


class DivAnswer(SimpleTextAnswer):
    """A division task answer."""

    def _create(self) -> None:
        self._answer = self._operand_1


class MulQuestion(SimpleTextQuestion):
    """A multiplication task question."""

    def _create(self) -> None:
        self._question = f'{self._operand_1} x {self._operand_2}'


class MulAnswer(SimpleTextAnswer):
    """A multiplication task answer."""

    def _create(self) -> None:
        self._answer = self._operand_1 * self._operand_2


class SubQuestion(SimpleTextQuestion):
    """A subtraction task question."""

    def _create(self) -> None:
        self._question = f'{self._operand_1} - {self._operand_2}'


class SubAnswer(SimpleTextAnswer):
    """A subtraction task answer."""

    def _create(self) -> None:
        self._answer = self._operand_1 - self._operand_2
