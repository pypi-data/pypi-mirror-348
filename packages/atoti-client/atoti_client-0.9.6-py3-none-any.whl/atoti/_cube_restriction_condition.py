from __future__ import annotations

from typing import Literal, TypeAlias

from ._constant import Scalar
from ._identification import LevelIdentifier
from ._operation.operation import (
    IsInCondition,
    LogicalCondition,
    RelationalCondition,
)

_CubeRestrictionLeafCondition: TypeAlias = (
    IsInCondition[LevelIdentifier, Literal["IS_IN"], Scalar]
    | RelationalCondition[LevelIdentifier, Literal["EQ"], Scalar]
)
CubeRestrictionCondition: TypeAlias = (
    _CubeRestrictionLeafCondition
    | LogicalCondition[_CubeRestrictionLeafCondition, Literal["AND"]]
)
