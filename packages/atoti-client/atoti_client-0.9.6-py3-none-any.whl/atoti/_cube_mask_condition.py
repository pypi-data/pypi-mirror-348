from typing import Literal, TypeAlias

from ._constant import Scalar
from ._identification import HierarchyIdentifier
from ._operation import (
    HierarchyIsInConditionBound,
    IsInCondition,
    IsInConditionOperatorBound,
    LogicalCondition,
)
from ._operation.operation import RelationalCondition

_CubeMaskLeafCondition: TypeAlias = (
    HierarchyIsInConditionBound
    | IsInCondition[HierarchyIdentifier, IsInConditionOperatorBound, Scalar]
    | RelationalCondition[HierarchyIdentifier, Literal["EQ", "NE"], Scalar]
)

CubeMaskCondition: TypeAlias = (
    _CubeMaskLeafCondition | LogicalCondition[_CubeMaskLeafCondition, Literal["AND"]]
)
