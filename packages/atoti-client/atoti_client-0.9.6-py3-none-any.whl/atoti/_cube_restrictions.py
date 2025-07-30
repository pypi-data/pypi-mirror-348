from __future__ import annotations

from collections.abc import Mapping, Sequence, Set as AbstractSet
from typing import Final, TypeAlias, final

from typing_extensions import override

from ._atoti_client import AtotiClient
from ._check_not_none import check_data_model_not_none, check_named_object_not_none
from ._collections import DelegatingMutableMapping
from ._constant import is_array
from ._cube_restriction_condition import (
    CubeRestrictionCondition,
    _CubeRestrictionLeafCondition,
)
from ._graphql_client import (
    CreateCubeRestrictionInput,
    CubeRestrictionFragmentConditionCubeRestrictionIsInCondition,
    CubeRestrictionFragmentConditionCubeRestrictionRelationalCondition,
    CubeRestrictionIsInConditionInput,
    CubeRestrictionIsInConditionOperator,
    CubeRestrictionLeafConditionInput,
    CubeRestrictionRelationalConditionInput,
    CubeRestrictionRelationalConditionOperator,
    DeleteCubeRestrictionInput,
)
from ._graphql_client.base_operation import GraphQLField
from ._graphql_client.custom_mutations import Mutation
from ._graphql_typename_field_name import (
    GRAPHQL_TYPENAME_FIELD_NAME as _GRAPHQL_TYPENAME_FIELD_NAME,
)
from ._identification import CubeIdentifier, LevelIdentifier, Role
from ._operation import (
    IsInCondition,
    RelationalCondition,
    condition_from_disjunctive_normal_form,
    disjunctive_normal_form_from_condition,
)
from ._require_live_extension import require_live_extension
from ._reserved_roles import check_no_reserved_roles
from ._transaction import get_data_model_transaction_id

_GraphQlCubeLeafCondition: TypeAlias = (
    CubeRestrictionFragmentConditionCubeRestrictionIsInCondition
    | CubeRestrictionFragmentConditionCubeRestrictionRelationalCondition
)


def _leaf_condition_from_graphql(
    condition: _GraphQlCubeLeafCondition, /
) -> _CubeRestrictionLeafCondition:
    match condition:
        case CubeRestrictionFragmentConditionCubeRestrictionIsInCondition():
            elements = {
                element for element in condition.elements if not is_array(element)
            }
            assert len(elements) == len(condition.elements)
            return IsInCondition.of(
                subject=LevelIdentifier._from_graphql(condition.level),
                operator=condition.is_in_operator.value,
                elements=elements,
            )
        case CubeRestrictionFragmentConditionCubeRestrictionRelationalCondition():
            assert not is_array(condition.target)
            return RelationalCondition(
                subject=LevelIdentifier._from_graphql(condition.level),
                operator=condition.relational_operator.value,
                target=condition.target,
            )


def _condition_from_graphql(
    dnf: Sequence[Sequence[_GraphQlCubeLeafCondition]],
    /,
) -> CubeRestrictionCondition:
    match dnf:
        case [graphql_conjunct_conditions]:
            conjunct_conditions = [
                _leaf_condition_from_graphql(condition)
                for condition in graphql_conjunct_conditions
            ]
            return condition_from_disjunctive_normal_form((conjunct_conditions,))
        case _:
            raise AssertionError(f"Unexpected disjunctive normal form: {dnf}.")


def _leaf_condition_to_graphql(
    condition: _CubeRestrictionLeafCondition, /
) -> CubeRestrictionLeafConditionInput:
    match condition:
        case IsInCondition():
            return CubeRestrictionLeafConditionInput(
                is_in=CubeRestrictionIsInConditionInput(
                    elements=list(condition.elements),
                    operator=CubeRestrictionIsInConditionOperator(condition.operator),
                    subject=condition.subject._graphql_input,
                )
            )
        case RelationalCondition():
            return CubeRestrictionLeafConditionInput(
                relational=CubeRestrictionRelationalConditionInput(
                    operator=CubeRestrictionRelationalConditionOperator(
                        condition.operator
                    ),
                    subject=condition.subject._graphql_input,
                    target=condition.target,
                )
            )


def _condition_to_graphql(
    condition: CubeRestrictionCondition, /
) -> list[list[CubeRestrictionLeafConditionInput]]:
    dnf = disjunctive_normal_form_from_condition(condition)
    return [
        [
            _leaf_condition_to_graphql(
                leaf_condition  # type: ignore[arg-type]
            )
            for leaf_condition in conjunct_conditions
        ]
        for conjunct_conditions in dnf
    ]


@final
class CubeRestrictions(DelegatingMutableMapping[Role, CubeRestrictionCondition]):
    def __init__(
        self, cube_identifier: CubeIdentifier, /, *, atoti_client: AtotiClient
    ) -> None:
        self._cube_identifier: Final = cube_identifier
        self._atoti_client: Final = atoti_client

    @override
    def _get_delegate(
        self, *, key: Role | None
    ) -> Mapping[str, CubeRestrictionCondition]:
        graphql_client = require_live_extension(self._atoti_client._graphql_client)
        data_model_transaction_id = get_data_model_transaction_id()

        if key is None:
            output = graphql_client.get_cube_restrictions(
                cube_name=self._cube_identifier.cube_name,
                data_model_transaction_id=data_model_transaction_id,
            )
            data_model = check_data_model_not_none(
                output.data_model,
                data_model_transaction_id=data_model_transaction_id,
            )
            cube = check_named_object_not_none(
                data_model.cube,
                "cube",
                self._cube_identifier.cube_name,
            )
            return {
                restriction.role: _condition_from_graphql(restriction.condition)
                for restriction in cube.restrictions
            }

        output = graphql_client.get_cube_restriction(  # type: ignore[assignment] # See https://github.com/python/mypy/issues/12968.
            cube_name=self._cube_identifier.cube_name,
            data_model_transaction_id=data_model_transaction_id,
            role=key,
        )
        data_model = check_data_model_not_none(
            output.data_model,
            data_model_transaction_id=data_model_transaction_id,
        )
        cube = check_named_object_not_none(
            data_model.cube,
            "cube",
            self._cube_identifier.cube_name,
        )
        return (
            {}
            if cube.restriction is None  # type: ignore[attr-defined]
            else {key: _condition_from_graphql(cube.restriction.condition)}  # type: ignore[attr-defined]
        )

    @override
    def _update_delegate(
        self, other: Mapping[Role, CubeRestrictionCondition], /
    ) -> None:
        check_no_reserved_roles(other)
        graphql_client = require_live_extension(self._atoti_client._graphql_client)
        data_model_transaction_id = get_data_model_transaction_id()

        fields: list[GraphQLField] = []
        for index, (role, condition) in enumerate(other.items()):
            output_fields = Mutation.create_cube_restriction(
                CreateCubeRestrictionInput(
                    condition=_condition_to_graphql(condition),
                    cube_name=self._cube_identifier.cube_name,
                    data_model_transaction_id=data_model_transaction_id,
                    role=role,
                )
            ).alias(f"createCubeRestriction_{index}")
            output_fields._subfields.append(GraphQLField(_GRAPHQL_TYPENAME_FIELD_NAME))
            fields.append(output_fields)

        graphql_client.mutation(*fields, operation_name="UpdateCubeRestrictions")

    @override
    def _delete_delegate_keys(self, keys: AbstractSet[Role], /) -> None:
        graphql_client = require_live_extension(self._atoti_client._graphql_client)
        data_model_transaction_id = get_data_model_transaction_id()

        fields: list[GraphQLField] = []
        for index, role in enumerate(keys):
            output_fields = Mutation.delete_cube_restriction(
                DeleteCubeRestrictionInput(
                    cube_name=self._cube_identifier.cube_name,
                    data_model_transaction_id=data_model_transaction_id,
                    role=role,
                )
            ).alias(f"deleteCubeRestriction_{index}")
            output_fields._subfields.append(GraphQLField(_GRAPHQL_TYPENAME_FIELD_NAME))
            fields.append(output_fields)

        graphql_client.mutation(*fields, operation_name="DeleteCubeRestrictions")
