from __future__ import annotations

from collections.abc import Callable
from typing import Final, Literal, final, overload

from typing_extensions import override

from .._constant import Constant
from .._data_type import DataType
from .._identification import ColumnName, ExternalColumnIdentifier
from .._operation import (
    IsInCondition,
    OperandConvertibleWithIdentifier,
    RelationalCondition,
)


@final
class ExternalColumn(OperandConvertibleWithIdentifier[ExternalColumnIdentifier]):
    """Column of an external table."""

    def __init__(
        self,
        identifier: ExternalColumnIdentifier,
        /,
        *,
        get_data_type: Callable[[], DataType],
    ) -> None:
        self._get_data_type: Final = get_data_type
        self.__identifier: Final = identifier

    @property
    def name(self) -> ColumnName:
        """The name of the column."""
        return self._identifier.column_name

    @property
    def data_type(self) -> DataType:
        """The type of the elements in the column."""
        return self._get_data_type()

    @property
    @override
    def _identifier(self) -> ExternalColumnIdentifier:
        return self.__identifier

    @property
    @override
    def _operation_operand(self) -> ExternalColumnIdentifier:
        return self._identifier

    @overload
    def isin(
        self,
        *elements: Constant,
    ) -> (
        IsInCondition[ExternalColumnIdentifier, Literal["IS_IN"], Constant]
        | RelationalCondition[ExternalColumnIdentifier, Literal["EQ"], Constant]
    ): ...

    @overload
    def isin(
        self,
        *elements: Constant | None,
    ) -> (
        IsInCondition[
            ExternalColumnIdentifier,
            Literal["IS_IN"],
            Constant | None,
        ]
        | RelationalCondition[ExternalColumnIdentifier, Literal["EQ"], Constant | None]
    ): ...

    def isin(
        self,
        *elements: Constant | None,
    ) -> (
        IsInCondition[ExternalColumnIdentifier, Literal["IS_IN"], Constant | None]
        | RelationalCondition[ExternalColumnIdentifier, Literal["EQ"], Constant | None]
    ):
        """Return a condition evaluating to ``True`` for elements of this column included in the given *elements*, and evaluating to ``False`` elsewhere.

        Args:
            elements: One or more values that the column elements will be compared against.

        """
        return IsInCondition.of(
            subject=self._operation_operand,
            operator="IS_IN",
            elements=set(elements),
        )
