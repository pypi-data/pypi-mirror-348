from __future__ import annotations

from typing import Literal, TypeAlias

from ._constant import Str
from ._identification import ColumnIdentifier
from ._operation import IsInCondition, LogicalCondition, RelationalCondition

_TablesRestrictionLeafCondition: TypeAlias = (
    IsInCondition[ColumnIdentifier, Literal["IS_IN"], Str]
    | RelationalCondition[ColumnIdentifier, Literal["EQ"], Str]
)
TablesRestrictionCondition: TypeAlias = (
    _TablesRestrictionLeafCondition
    | LogicalCondition[_TablesRestrictionLeafCondition, Literal["AND"]]
)
