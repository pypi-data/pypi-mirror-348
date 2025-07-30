from __future__ import annotations

from collections import defaultdict
from collections.abc import Mapping, Sequence, Set as AbstractSet
from typing import Final, TypeAlias, final

from typing_extensions import override

from ._atoti_client import AtotiClient
from ._check_not_none import check_data_model_not_none, check_named_object_not_none
from ._collections import DelegatingConvertingMapping, SupportsUncheckedMappingLookup
from ._graphql_client import (
    CreateHierarchyInput,
    DeleteHierarchyInput,
    HierarchyDefinition,
    SelectionHierarchyDefinition,
    SelectionHierarchyLevelDefinition,
)
from ._graphql_client.base_operation import GraphQLField
from ._graphql_client.custom_mutations import Mutation
from ._graphql_typename_field_name import (
    GRAPHQL_TYPENAME_FIELD_NAME as _GRAPHQL_TYPENAME_FIELD_NAME,
)
from ._identification import (
    RESERVED_DIMENSION_NAMES as _RESERVED_DIMENSION_NAMES,
    ColumnIdentifier,
    CubeIdentifier,
    DimensionIdentifier,
    DimensionName,
    HierarchyIdentifier,
    HierarchyKey,
    HierarchyName,
    HierarchyUnambiguousKey,
    LevelIdentifier,
    LevelName,
)
from ._ipython import ReprJson, ReprJsonable
from ._java_api import JavaApi
from ._require_live_extension import require_live_extension
from ._transaction import get_data_model_transaction_id
from .column import Column
from .hierarchy import Hierarchy
from .level import Level

_HierarchyConvertibleElement: TypeAlias = Column | Level
_HierarchyConvertible: TypeAlias = (
    Sequence[_HierarchyConvertibleElement]
    | Mapping[LevelName, _HierarchyConvertibleElement]
)


def _get_column_identifier(
    element: _HierarchyConvertibleElement,
    /,
) -> ColumnIdentifier:
    match element:
        case Column():
            return element._identifier
        case Level():
            selection_field = element._selection_field
            assert selection_field is not None
            return selection_field.column_identifier


def _infer_dimension_name(element: _HierarchyConvertibleElement, /) -> DimensionName:
    identifier = element._identifier
    match identifier:
        case ColumnIdentifier():
            return identifier.table_identifier.table_name
        case LevelIdentifier():
            return identifier.hierarchy_identifier.dimension_identifier.dimension_name


def _normalize_key(key: HierarchyKey, /) -> tuple[DimensionName | None, HierarchyName]:
    return (None, key) if isinstance(key, str) else key


@final
class Hierarchies(
    SupportsUncheckedMappingLookup[HierarchyKey, HierarchyUnambiguousKey, Hierarchy],
    DelegatingConvertingMapping[
        HierarchyKey,
        HierarchyUnambiguousKey,
        Hierarchy,
        _HierarchyConvertible,
    ],
    ReprJsonable,
):
    """Manage the hierarchies of a :class:`~atoti.Cube`.

    Example:
        .. doctest::
            :hide:

            >>> session = getfixture("default_session")

        >>> prices_df = pd.DataFrame(
        ...     columns=["Nation", "City", "Color", "Price"],
        ...     data=[
        ...         ("France", "Paris", "red", 20.0),
        ...         ("France", "Lyon", "blue", 15.0),
        ...         ("France", "Toulouse", "green", 10.0),
        ...         ("UK", "London", "red", 20.0),
        ...         ("UK", "Manchester", "blue", 15.0),
        ...     ],
        ... )
        >>> table = session.read_pandas(prices_df, table_name="Prices")
        >>> cube = session.create_cube(table, mode="manual")
        >>> h = cube.hierarchies
        >>> h["Nation"] = {"Nation": table["Nation"]}
        >>> list(h)
        [('Prices', 'Nation')]

        A hierarchy can be renamed by copying it and deleting the old one:

        >>> h["Country"] = h["Nation"]
        >>> del h["Nation"]
        >>> list(h)
        [('Prices', 'Country')]
        >>> list(h["Country"])
        ['Nation']

        :meth:`~dict.update` can be used to batch hierarchy creation operations for improved performance:

        >>> h.update(
        ...     {
        ...         ("Geography", "Geography"): [table["Nation"], table["City"]],
        ...         "Color": {"Color": table["Color"]},
        ...     }
        ... )
        >>> sorted(h)
        [('Geography', 'Geography'), ('Prices', 'Color'), ('Prices', 'Country')]

    See Also:
        :class:`~atoti.Hierarchy` to configure existing hierarchies.
    """

    def __init__(
        self,
        *,
        atoti_client: AtotiClient,
        cube_identifier: CubeIdentifier,
        java_api: JavaApi | None,
    ) -> None:
        self._atoti_client: Final = atoti_client
        self._cube_identifier: Final = cube_identifier
        self._java_api: Final = java_api

    @override
    def _create_lens(self, key: HierarchyUnambiguousKey, /) -> Hierarchy:
        dimension_name, hierarchy_name = key
        return Hierarchy(
            HierarchyIdentifier(DimensionIdentifier(dimension_name), hierarchy_name),
            atoti_client=self._atoti_client,
            cube_identifier=self._cube_identifier,
            java_api=self._java_api,
        )

    @override
    def _get_unambiguous_keys(
        self,
        *,
        key: HierarchyKey | None,
    ) -> list[HierarchyUnambiguousKey]:
        dimension_name, hierarchy_name = (
            (None, None) if key is None else _normalize_key(key)
        )

        # Remove `not self._java_api` once query sessions are supported.
        if not self._java_api or not self._atoti_client._graphql_client:
            cube_discovery = self._atoti_client.get_cube_discovery()
            return [
                (dimension.name, hierarchy.name)
                for dimension in cube_discovery.cubes[
                    self._cube_identifier.cube_name
                ].dimensions
                if dimension.name not in _RESERVED_DIMENSION_NAMES
                and (dimension_name is None or dimension.name == dimension_name)
                for hierarchy in dimension.hierarchies
                if hierarchy_name is None or hierarchy.name == hierarchy_name
            ]

        data_model_transaction_id = get_data_model_transaction_id()

        if hierarchy_name is None:
            output = self._atoti_client._graphql_client.get_hierarchies(
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
            return [
                (dimension.name, hierarchy.name)
                for dimension in cube.dimensions
                if dimension.name not in _RESERVED_DIMENSION_NAMES
                for hierarchy in dimension.hierarchies
            ]

        if dimension_name is None:
            output = (
                self._atoti_client._graphql_client.find_hierarchy_across_dimensions(  # type: ignore[assignment] # See https://github.com/python/mypy/issues/12968.
                    cube_name=self._cube_identifier.cube_name,
                    data_model_transaction_id=data_model_transaction_id,
                    hierarchy_name=hierarchy_name,
                )
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
            return [
                (dimension.name, dimension.hierarchy.name)  # type: ignore[attr-defined]
                for dimension in cube.dimensions
                if dimension.name not in _RESERVED_DIMENSION_NAMES
                and dimension.hierarchy  # type: ignore[attr-defined]
            ]

        output = self._atoti_client._graphql_client.find_hierarchy(  # type: ignore[assignment] # See https://github.com/python/mypy/issues/12968.
            cube_name=self._cube_identifier.cube_name,
            data_model_transaction_id=data_model_transaction_id,
            dimension_name=dimension_name,
            hierarchy_name=hierarchy_name,
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
            [HierarchyIdentifier._from_graphql(cube.dimension.hierarchy).key]  # type: ignore[attr-defined]
            if cube.dimension  # type: ignore[attr-defined]
            and cube.dimension.hierarchy  # type: ignore[attr-defined]
            and cube.dimension.hierarchy.dimension.name not in _RESERVED_DIMENSION_NAMES  # type: ignore[attr-defined]
            else []
        )

    @override
    def _update_delegate(
        self,
        other: Mapping[
            HierarchyKey,
            # `None` means delete the hierarchy at this key.
            _HierarchyConvertible | None,
        ],
        /,
    ) -> None:
        deleted: dict[DimensionName, set[HierarchyName]] = defaultdict(set)
        updated: dict[
            DimensionName,
            dict[HierarchyName, Mapping[LevelName, _HierarchyConvertibleElement]],
        ] = defaultdict(
            dict,
        )

        for hierarchy_key, elements in other.items():
            dimension_name, hierarchy_name = _normalize_key(hierarchy_key)

            if elements is None:
                if dimension_name is None:
                    dimension_name = self[hierarchy_name].dimension

                deleted[dimension_name].add(hierarchy_name)
            else:
                normalized_elements: Mapping[
                    LevelName, _HierarchyConvertibleElement
                ] = (
                    elements
                    if isinstance(elements, Mapping)
                    else {
                        level_or_column.name: level_or_column
                        for level_or_column in elements
                    }
                )

                if dimension_name is None:
                    assert (hierarchy_name in self) is not None, (
                        f"Expected zero or one hierarchy named `{hierarchy_name}` across all dimensions."
                    )
                    dimension_name = _infer_dimension_name(
                        next(iter(normalized_elements.values())),
                    )

                updated[dimension_name][hierarchy_name] = normalized_elements

        updated_with_levels_only: dict[
            DimensionName,
            dict[HierarchyName, Mapping[LevelName, Level]],
        ] = {
            dimension_name: {
                hierarchy_name: {
                    level_name: element
                    for level_name, element in levels.items()
                    if isinstance(element, Level)
                }
                for hierarchy_name, levels in hierarchies.items()
            }
            for dimension_name, hierarchies in updated.items()
        }
        updated_contains_levels_only = {
            dimension_name: {
                hierarchy_name: len(elements)
                for hierarchy_name, elements in hierarchies.items()
            }
            for dimension_name, hierarchies in updated.items()
        } == {
            dimension_name: {
                hierarchy_name: len(elements)
                for hierarchy_name, elements in hierarchies.items()
            }
            for dimension_name, hierarchies in updated_with_levels_only.items()
        }

        if deleted or not updated_contains_levels_only:
            java_api = require_live_extension(self._java_api)

            java_api.update_hierarchies_for_cube(
                self._cube_identifier.cube_name,
                deleted=deleted,
                updated={
                    dimension_name: {
                        hierarchy_name: {
                            level_name: _get_column_identifier(element)
                            for level_name, element in levels.items()
                        }
                        for hierarchy_name, levels in hierarchy.items()
                    }
                    for dimension_name, hierarchy in updated.items()
                },
            )
            java_api.refresh()
            return

        graphql_client = require_live_extension(self._atoti_client._graphql_client)
        data_model_transaction_id = get_data_model_transaction_id()

        fields: list[GraphQLField] = []
        for index, (dimension_name, hierarchies) in enumerate(
            updated_with_levels_only.items()
        ):
            for hierarchy_name, levels in hierarchies.items():
                level_definitions: list[SelectionHierarchyLevelDefinition] = []

                for level_name, level in levels.items():
                    selection_field = level._selection_field
                    assert selection_field is not None
                    level_definitions.append(
                        SelectionHierarchyLevelDefinition(
                            level_name=level_name,
                            selection_field_identifier=selection_field._identifier._graphql_input,
                        )
                    )

                output_fields = Mutation.create_hierarchy(
                    CreateHierarchyInput(
                        cube_name=self._cube_identifier.cube_name,
                        data_model_transaction_id=data_model_transaction_id,
                        definition=HierarchyDefinition(
                            selection=SelectionHierarchyDefinition(
                                levels=level_definitions
                            )
                        ),
                        hierarchy_identifier=HierarchyIdentifier(
                            DimensionIdentifier(dimension_name),
                            hierarchy_name=hierarchy_name,
                        )._graphql_input,
                    ),
                ).alias(f"createHierarchy_{index}")
                output_fields._subfields.append(
                    GraphQLField(_GRAPHQL_TYPENAME_FIELD_NAME)
                )
                fields.append(output_fields)

        graphql_client.mutation(*fields, operation_name="UpdateHierarchies")

    @override
    def _delete_delegate_keys(self, keys: AbstractSet[HierarchyKey], /) -> None:
        graphql_client = require_live_extension(self._atoti_client._graphql_client)
        data_model_transaction_id = get_data_model_transaction_id()

        hierarchy_identifiers: set[HierarchyIdentifier] = set()

        for key in keys:
            match key:
                case dimension_name, hierarchy_name:
                    hierarchy_identifiers.add(
                        HierarchyIdentifier(
                            DimensionIdentifier(dimension_name), hierarchy_name
                        )
                    )
                case _:
                    hierarchy_identifier = self[key]._identifier
                    hierarchy_identifiers.add(hierarchy_identifier)

        fields: list[GraphQLField] = []
        for index, hierarchy_identifier in enumerate(hierarchy_identifiers):
            output_fields = Mutation.delete_hierarchy(
                DeleteHierarchyInput(
                    cube_name=self._cube_identifier.cube_name,
                    data_model_transaction_id=data_model_transaction_id,
                    hierarchy_identifier=hierarchy_identifier._graphql_input,
                ),
            ).alias(f"deleteHierarchy_{index}")
            output_fields._subfields.append(GraphQLField(_GRAPHQL_TYPENAME_FIELD_NAME))
            fields.append(output_fields)
        graphql_client.mutation(*fields, operation_name="DeleteHierarchies")

    @override
    def _repr_json_(self) -> ReprJson:
        dimensions: dict[DimensionName, list[Hierarchy]] = defaultdict(list)
        for hierarchy in self.values():
            dimensions[hierarchy.dimension].append(hierarchy)
        json = {
            dimension: dict(
                sorted(
                    {
                        hierarchy._repr_json_()[1]["root"]: hierarchy._repr_json_()[0]
                        for hierarchy in dimension_hierarchies
                    }.items(),
                ),
            )
            for dimension, dimension_hierarchies in sorted(dimensions.items())
        }
        return json, {"expanded": True, "root": "Dimensions"}
