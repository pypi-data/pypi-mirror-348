from __future__ import annotations

from collections.abc import Mapping, Set as AbstractSet
from typing import Final, final

from typing_extensions import override

from ._collections import DelegatingMutableMapping
from ._constant import Scalar
from ._cube_mask_condition import CubeMaskCondition, _CubeMaskLeafCondition
from ._identification import CubeName, Role
from ._java_api import JavaApi
from ._operation import disjunctive_normal_form_from_condition
from ._operation.operation import (
    HierarchyIsInCondition,
    IsInCondition,
    RelationalCondition,
)
from ._require_live_extension import require_live_extension


@final
class Masks(DelegatingMutableMapping[Role, CubeMaskCondition]):
    def __init__(self, /, *, cube_name: CubeName, java_api: JavaApi | None) -> None:
        self._cube_name: Final = cube_name
        self._java_api: Final = java_api

    @override
    def _get_delegate(self, *, key: Role | None) -> Mapping[Role, CubeMaskCondition]:
        java_api = require_live_extension(self._java_api)
        return java_api.get_cube_mask(key, cube_name=self._cube_name)

    @override
    def _update_delegate(self, other: Mapping[Role, CubeMaskCondition], /) -> None:  # noqa: C901
        java_api = require_live_extension(self._java_api)

        for role, condition in other.items():
            dnf: tuple[tuple[_CubeMaskLeafCondition, ...]] = (
                disjunctive_normal_form_from_condition(condition)
            )
            (conjunct_conditions,) = dnf

            included_members: dict[str, AbstractSet[Scalar]] = {}
            included_member_paths: dict[str, AbstractSet[tuple[Scalar, ...]]] = {}
            excluded_members: dict[str, AbstractSet[Scalar]] = {}
            excluded_member_paths: dict[str, AbstractSet[tuple[Scalar, ...]]] = {}

            for leaf_condition in conjunct_conditions:
                hierarchy_java_description = leaf_condition.subject._java_description

                match leaf_condition:
                    case HierarchyIsInCondition(
                        operator=operator, member_paths=member_paths
                    ):
                        match operator:
                            case "IS_IN":
                                included_member_paths[hierarchy_java_description] = (
                                    member_paths
                                )
                            case "IS_NOT_IN":
                                excluded_member_paths[hierarchy_java_description] = (
                                    member_paths
                                )
                    case IsInCondition(operator=operator, elements=elements):
                        match operator:
                            case "IS_IN":
                                included_members[hierarchy_java_description] = elements
                            case "IS_NOT_IN":
                                excluded_members[hierarchy_java_description] = elements
                    case RelationalCondition(operator=operator, target=target):
                        match operator:
                            case "EQ":
                                included_members[hierarchy_java_description] = {target}
                            case "NE":
                                excluded_members[hierarchy_java_description] = {target}

            java_api.set_cube_mask(
                role,
                cube_name=self._cube_name,
                included_members=included_members,
                included_member_paths=included_member_paths,
                excluded_members=excluded_members,
                excluded_member_paths=excluded_member_paths,
            )

    @override
    def _delete_delegate_keys(self, keys: AbstractSet[Role], /) -> None:
        raise NotImplementedError("Cannot delete masking value.")
