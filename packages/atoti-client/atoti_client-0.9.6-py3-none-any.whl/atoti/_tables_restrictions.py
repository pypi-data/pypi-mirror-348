from __future__ import annotations

from collections import defaultdict
from collections.abc import Mapping, Set as AbstractSet
from pathlib import Path
from typing import Final, TypeAlias, final

from typing_extensions import override

from ._collections import DelegatingMutableMapping
from ._content_client import (
    SECURITY_ROOT_DIRECTORY,
    ContentClient,
    ContentTree,
    DirectoryContentTree,
    FileContentTree,
)
from ._identification import (
    ColumnIdentifier,
    ColumnName,
    Role,
    TableIdentifier,
    TableName,
)
from ._operation import (
    IsInCondition,
    RelationalCondition,
    condition_from_disjunctive_normal_form,
    disjunctive_normal_form_from_condition,
)
from ._pydantic import get_type_adapter
from ._reserved_roles import ROLE_ADMIN, check_no_reserved_roles
from ._tables_restriction_condition import (
    TablesRestrictionCondition,
    _TablesRestrictionLeafCondition,
)

_DIRECTORY = f"{SECURITY_ROOT_DIRECTORY}/column_restrictions"
_PATH_TEMPLATE = f"{_DIRECTORY}/{{role}}.json"

_SerializedCondition: TypeAlias = Mapping[
    TableName, Mapping[ColumnName, AbstractSet[str]]
]


def _deserialize_condition(
    serialized_condition: _SerializedCondition, /
) -> TablesRestrictionCondition:
    conjunct_conditions = [
        IsInCondition.of(
            subject=ColumnIdentifier(TableIdentifier(table_name), column_name),
            operator="IS_IN",
            elements=elements,
        )
        for table_name, column_restriction in serialized_condition.items()
        for column_name, elements in column_restriction.items()
    ]
    return condition_from_disjunctive_normal_form((conjunct_conditions,))


def _condition_from_content_tree(
    tree: ContentTree,
    /,
) -> TablesRestrictionCondition:
    assert isinstance(tree, FileContentTree)
    serialized_condition = get_type_adapter(_SerializedCondition).validate_json(  # type: ignore[type-abstract]
        tree.entry.content
    )
    return _deserialize_condition(serialized_condition)


def _serialize_condition(
    condition: TablesRestrictionCondition,
) -> dict[TableName, dict[ColumnName, list[str]]]:
    result: dict[TableName, dict[ColumnName, list[str]]] = defaultdict(dict)

    dnf: tuple[tuple[_TablesRestrictionLeafCondition, ...]] = (
        disjunctive_normal_form_from_condition(condition)
    )
    (conjunct_conditions,) = dnf

    for leaf_condition in conjunct_conditions:
        match leaf_condition:
            case IsInCondition(subject=subject, operator="IS_IN", elements=elements):
                result[subject.table_identifier.table_name][subject.column_name] = list(
                    elements
                )
            case RelationalCondition(subject=subject, operator="EQ", target=target):
                result[subject.table_identifier.table_name][subject.column_name] = [
                    target
                ]

    return result


@final
class Restrictions(DelegatingMutableMapping[Role, TablesRestrictionCondition]):
    def __init__(self, *, content_client: ContentClient) -> None:
        self._content_client: Final = content_client

    @override
    def _get_delegate(
        self, *, key: Role | None
    ) -> Mapping[Role, TablesRestrictionCondition]:
        path = _DIRECTORY if key is None else _PATH_TEMPLATE.format(role=key)
        tree = self._content_client.get(path)

        if not tree:
            return {}

        if key is None:
            assert isinstance(tree, DirectoryContentTree)
            return {
                Path(filename).stem: _condition_from_content_tree(child_tree)
                for filename, child_tree in tree.children.items()
            }

        return {key: _condition_from_content_tree(tree)}

    @override
    def _update_delegate(
        self, other: Mapping[Role, TablesRestrictionCondition], /
    ) -> None:
        check_no_reserved_roles(other)

        for role, condition in other.items():
            path = _PATH_TEMPLATE.format(role=role)
            content = _serialize_condition(condition)

            self._content_client.create(
                path,
                content=content,
                owners={ROLE_ADMIN},
                readers={ROLE_ADMIN},
            )

    @override
    def _delete_delegate_keys(self, keys: AbstractSet[Role], /) -> None:
        for role in keys:
            path = _PATH_TEMPLATE.format(role=role)
            self._content_client.delete(path)
