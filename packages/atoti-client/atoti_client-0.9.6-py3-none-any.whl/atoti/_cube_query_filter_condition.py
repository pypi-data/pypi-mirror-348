from __future__ import annotations

from typing import Literal, TypeAlias

from ._constant import Constant, Scalar
from ._identification import HierarchyIdentifier, LevelIdentifier, MeasureIdentifier
from ._operation import (
    HierarchyIsInCondition,
    IsInCondition,
    IsInConditionOperatorBound,
    LogicalCondition,
    RelationalCondition,
    RelationalConditionOperatorBound,
)

_CubeQueryFilterHierarchyIsInCondition: TypeAlias = HierarchyIsInCondition[
    Literal["IS_IN"], Scalar
]
_CubeQueryFilterIsInHierarchyCondition: TypeAlias = IsInCondition[
    HierarchyIdentifier, IsInConditionOperatorBound, Scalar
]
_CubeQueryFilterIsInLevelCondition: TypeAlias = IsInCondition[
    LevelIdentifier, IsInConditionOperatorBound, Scalar
]
_CubeQueryFilterIsInMeasureCondition: TypeAlias = IsInCondition[
    MeasureIdentifier, IsInConditionOperatorBound, Constant | None
]
_CubeQueryFilterRelationalHierarchyCondition: TypeAlias = RelationalCondition[
    HierarchyIdentifier, Literal["EQ", "NE"], Scalar
]
_CubeQueryFilterRelationalLevelCondition: TypeAlias = RelationalCondition[
    LevelIdentifier, RelationalConditionOperatorBound, Scalar
]
_CubeQueryFilterRelationalMeasureCondition: TypeAlias = RelationalCondition[
    MeasureIdentifier, RelationalConditionOperatorBound, Constant | None
]
_CubeQueryFilterLeafCondition: TypeAlias = (
    _CubeQueryFilterHierarchyIsInCondition
    | _CubeQueryFilterIsInHierarchyCondition
    | _CubeQueryFilterIsInLevelCondition
    | _CubeQueryFilterIsInMeasureCondition
    | _CubeQueryFilterRelationalHierarchyCondition
    | _CubeQueryFilterRelationalLevelCondition
    | _CubeQueryFilterRelationalMeasureCondition
)
CubeQueryFilterCondition: TypeAlias = (
    _CubeQueryFilterLeafCondition
    | LogicalCondition[_CubeQueryFilterLeafCondition, Literal["AND"]]
)
