from __future__ import annotations

from collections.abc import Callable, Iterator, Mapping, MutableMapping
from typing import Final, Literal, NoReturn, final, overload

from pydantic import JsonValue
from typing_extensions import deprecated, override

from ._atoti_client import AtotiClient
from ._check_not_none import check_data_model_not_none, check_named_object_not_none
from ._constant import ScalarT_co
from ._deprecated_warning_category import (
    DEPRECATED_WARNING_CATEGORY as _DEPRECATED_WARNING_CATEGORY,
)
from ._doc import doc
from ._graphql_client import UpdateHierarchyInput
from ._hierarchy_properties import HierarchyProperties
from ._identification import (
    CubeIdentifier,
    DimensionIdentifier,
    DimensionName,
    HasIdentifier,
    HierarchyIdentifier,
    HierarchyName,
    LevelIdentifier,
    LevelName,
    check_not_reserved_dimension_name,
)
from ._ipython import ReprJson, ReprJsonable
from ._java_api import JavaApi
from ._operation import HierarchyIsInCondition, IsInCondition
from ._operation.operation import RelationalCondition
from ._require_live_extension import require_live_extension
from ._transaction import get_data_model_transaction_id
from .level import Level

_FORCE_VIRTUAL_PROPERTY_NAME = "activeviam.experimental.forceVirtualHierarchies"
_VIRTUAL_HIERARCHY_CARDINALITY_THRESHOLD = 10_000


@final
class Hierarchy(
    Mapping[LevelName, Level],
    HasIdentifier[HierarchyIdentifier],
    ReprJsonable,
):
    """Hierarchy of a :class:`~atoti.Cube`.

    A hierarchy is a sub category of a :attr:`~dimension` and represents a precise type of data.

    For example, :guilabel:`Quarter` or :guilabel:`Week` could be hierarchies in the :guilabel:`Time` dimension.

    See Also:
        :class:`~atoti.hierarchies.Hierarchies` to define one.
    """

    def __init__(
        self,
        identifier: HierarchyIdentifier,
        /,
        *,
        atoti_client: AtotiClient,
        cube_identifier: CubeIdentifier,
        java_api: JavaApi | None,
    ) -> None:
        self._atoti_client: Final = atoti_client
        self._cube_identifier: Final = cube_identifier
        self.__identifier = identifier
        self._java_api: Final = java_api

    @final
    def __bool__(self) -> NoReturn:
        raise RuntimeError(
            "Hierarchies cannot be cast to a boolean. Use `.isin()` method or a relational operator to create a condition instead.",
        )

    @override
    def __hash__(self) -> int:
        # See comment in `OperandConvertible.__hash__()`.
        return id(self)

    @final
    @override
    # The signature is not compatible with `object.__eq__()` on purpose.
    def __eq__(  # type: ignore[override] # pyright: ignore[reportIncompatibleMethodOverride]
        self,
        other: ScalarT_co,  # type: ignore[misc]
        /,
    ) -> RelationalCondition[HierarchyIdentifier, Literal["EQ"], ScalarT_co]:
        assert other is not None, "Use `isnull()` instead."
        return RelationalCondition(
            subject=self._identifier, operator="EQ", target=other
        )

    @final
    @override
    # The signature is not compatible with `object.__ne__()` on purpose.
    def __ne__(  # type: ignore[override] # pyright: ignore[reportIncompatibleMethodOverride]
        self,
        other: ScalarT_co,  # type: ignore[misc]
        /,
    ) -> RelationalCondition[HierarchyIdentifier, Literal["NE"], ScalarT_co]:
        assert other is not None, "Use `isnull()` instead."
        return RelationalCondition(
            subject=self._identifier, operator="NE", target=other
        )

    @property
    def dimension(self) -> DimensionName:
        """Name of the dimension of the hierarchy.

        A dimension is a logical group of attributes (e.g. :guilabel:`Geography`).
        It can be thought of as a folder containing hierarchies.

        Note:
            If all the hierarchies in a dimension have their deepest level of type ``TIME``, the dimension's type will be set to ``TIME`` too.
            This can be useful for some clients such as Excel which rely on the dimension's type to be ``TIME`` to decide whether to display date filters.
        """
        return self._identifier.dimension_identifier.dimension_name

    @dimension.setter
    def dimension(self, value: DimensionName, /) -> None:
        check_not_reserved_dimension_name(value)

        java_api = require_live_extension(self._java_api)
        java_api.update_hierarchy_dimension(
            self._identifier,
            value,
            cube_name=self._cube_identifier.cube_name,
        )
        java_api.refresh()
        self.__identifier = HierarchyIdentifier(DimensionIdentifier(value), self.name)

    @property
    def dimension_default(self) -> bool:
        """Whether the hierarchy is the default in its :attr:`~atoti.Hierarchy.dimension` or not.

        Some UIs support clicking on a dimension (or drag and dropping it) as a shortcut to add its default hierarchy to a widget.

        Example:
            .. doctest::
                :hide:

                >>> session = getfixture("default_session")

            >>> table = session.create_table(
            ...     "Sales",
            ...     data_types={
            ...         "Product": "String",
            ...         "Shop": "String",
            ...         "Customer": "String",
            ...         "Date": "LocalDate",
            ...     },
            ... )
            >>> cube = session.create_cube(table, mode="manual")
            >>> h = cube.hierarchies
            >>> for column_name in table:
            ...     h[column_name] = [table[column_name]]
            ...     assert h[column_name].dimension == table.name

            By default, the default hierarchy of a dimension is the first created one:

            >>> h["Product"].dimension_default
            True
            >>> h["Shop"].dimension_default
            False
            >>> h["Customer"].dimension_default
            False
            >>> h["Date"].dimension_default
            False

            There can only be one default hierarchy per dimension:

            >>> h["Shop"].dimension_default = True
            >>> h["Product"].dimension_default
            False
            >>> h["Shop"].dimension_default
            True
            >>> h["Customer"].dimension_default
            False
            >>> h["Date"].dimension_default
            False

            When the default hierarchy is deleted, the first created remaining one becomes the default:

            >>> del h["Shop"]
            >>> h["Product"].dimension_default
            True
            >>> h["Customer"].dimension_default
            False
            >>> h["Date"].dimension_default
            False

            The same thing occurs if the default hierarchy is moved to another dimension:

            >>> h["Product"].dimension = "Product"
            >>> h["Customer"].dimension_default
            True
            >>> h["Date"].dimension_default
            False

            Since :guilabel:`Product` is the first created hierarchy of the newly created dimension, it is the default one there:

            >>> h["Product"].dimension_default
            True

        """
        if not self._atoti_client._graphql_client:
            cube_discovery = self._atoti_client.get_cube_discovery()
            return (
                cube_discovery.cubes[self._cube_identifier.cube_name]
                .name_to_dimension[self.dimension]
                .default_hierarchy
                == self.name
            )

        data_model_transaction_id = get_data_model_transaction_id()

        output = self._atoti_client._graphql_client.get_dimension_default_hierarchy(
            cube_name=self._cube_identifier.cube_name,
            data_model_transaction_id=data_model_transaction_id,
            dimension_name=self.dimension,
        )
        data_model = check_data_model_not_none(
            output.data_model, data_model_transaction_id=data_model_transaction_id
        )
        cube = check_named_object_not_none(
            data_model.cube,
            "cube",
            self._cube_identifier.cube_name,
        )
        dimension = check_named_object_not_none(
            cube.dimension,
            "dimension",
            self.dimension,
        )
        return dimension.default_hierarchy.name == self.name

    @dimension_default.setter
    def dimension_default(self, dimension_default: bool, /) -> None:
        java_api = require_live_extension(self._java_api)
        java_api.set_hierarchy_dimension_default(
            self._identifier,
            dimension_default,
            cube_name=self._cube_identifier.cube_name,
        )
        java_api.refresh()
        self._dimension_default = dimension_default

    @property
    @override
    def _identifier(self) -> HierarchyIdentifier:
        return self.__identifier

    @overload
    def isin(
        self,
        *members: ScalarT_co,  # type: ignore[misc]
    ) -> (
        IsInCondition[HierarchyIdentifier, Literal["IS_IN"], ScalarT_co]
        | RelationalCondition[HierarchyIdentifier, Literal["EQ"], ScalarT_co]
    ): ...

    @overload
    def isin(
        self,
        *member_paths: tuple[ScalarT_co, ...],
    ) -> HierarchyIsInCondition[Literal["IS_IN"], ScalarT_co]: ...

    def isin(
        self,
        *members_or_member_paths: ScalarT_co | tuple[ScalarT_co, ...],
    ) -> (
        HierarchyIsInCondition[Literal["IS_IN"], ScalarT_co]
        | IsInCondition[HierarchyIdentifier, Literal["IS_IN"], ScalarT_co]
        | RelationalCondition[HierarchyIdentifier, Literal["EQ"], ScalarT_co]
    ):
        """Return a condition evaluating to ``True`` where this hierarchy's current member (or its path) is included in the given *members* (or *member_paths*), and evaluating to ``False`` elsewhere.

        Args:
            members_or_member_paths: Either:

                * One or more members.
                  In that case, all the hierarchy's members are expected to be unique across all the levels of the hierarchy.
                * One or more member paths expressed as tuples of members starting from the top of the hierarchy.

        Example:
            .. doctest::
                :hide:

                >>> session = getfixture("default_session")

            >>> df = pd.DataFrame(
            ...     columns=["Country", "City", "Price"],
            ...     data=[
            ...         ("Germany", "Berlin", 150.0),
            ...         ("Germany", "Hamburg", 120.0),
            ...         ("United Kingdom", "Bath", 240.0),
            ...         ("United Kingdom", "London", 270.0),
            ...     ],
            ... )
            >>> table = session.read_pandas(
            ...     df, keys={"Country", "City"}, table_name="Example"
            ... )
            >>> cube = session.create_cube(table, mode="manual")
            >>> h = cube.hierarchies
            >>> h["Geography"] = [table["Country"], table["City"]]

            Condition on members:

            >>> h["Geography"].isin("Germany", "London")
            h['Example', 'Geography'].isin('Germany', 'London')

            Condition on member paths:

            >>> h["Geography"].isin(("Germany",), ("United Kingdom", "Bath"))
            h['Example', 'Geography'].isin(('Germany',), ('United Kingdom', 'Bath'))

            Members and member paths cannot be mixed:

            >>> h["Geography"].isin("Germany", ("United Kingdom", "Bath"))
            Traceback (most recent call last):
                ...
            ValueError: Expected either only members or only member paths but both were mixed: `('Germany', ('United Kingdom', 'Bath'))`.

            Conditions on single members are normalized to equality conditions:

            >>> h["Geography"].isin("Germany")
            h['Example', 'Geography'] == 'Germany'

        """
        member_paths = frozenset(
            member_or_member_path
            for member_or_member_path in members_or_member_paths
            if isinstance(member_or_member_path, tuple)
        )
        if len(member_paths) == len(members_or_member_paths):
            return HierarchyIsInCondition(
                subject=self._identifier,
                operator="IS_IN",
                member_paths=member_paths,
                level_names=list(self),
            )

        members = frozenset(
            member_or_member_path
            for member_or_member_path in members_or_member_paths
            if not isinstance(member_or_member_path, tuple)
        )
        if len(members) != len(members_or_member_paths):
            raise ValueError(
                f"Expected either only members or only member paths but both were mixed: `{members_or_member_paths}`."
            )

        return IsInCondition.of(
            subject=self._identifier, operator="IS_IN", elements=members
        )

    def _get_level_names(self, *, key: LevelName | None) -> list[LevelName]:
        # Remove `not self._java_api` once query sessions are supported.
        if not self._java_api or not self._atoti_client._graphql_client:
            cube_discovery = self._atoti_client.get_cube_discovery()
            return [
                level.name
                for level in cube_discovery.cubes[self._cube_identifier.cube_name]
                .name_to_dimension[self.dimension]
                .name_to_hierarchy[self.name]
                .levels
                if level.type != "ALL" and (key is None or level.name == key)
            ]

        data_model_transaction_id = get_data_model_transaction_id()

        if key is None:
            output = self._atoti_client._graphql_client.get_hierarchy_levels(
                cube_name=self._cube_identifier.cube_name,
                data_model_transaction_id=data_model_transaction_id,
                dimension_name=self.dimension,
                hierarchy_name=self.name,
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
            dimension = check_named_object_not_none(
                cube.dimension,
                "dimension",
                self.dimension,
            )
            hierarchy = check_named_object_not_none(
                dimension.hierarchy,
                "hierarchy",
                self.name,
            )
            return [
                level.name for level in hierarchy.levels if level.type.value != "ALL"
            ]

        output = self._atoti_client._graphql_client.find_level(  # type: ignore[assignment] # See https://github.com/python/mypy/issues/12968.
            cube_name=self._cube_identifier.cube_name,
            data_model_transaction_id=data_model_transaction_id,
            dimension_name=self.dimension,
            hierarchy_name=self.name,
            level_name=key,
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
        dimension = check_named_object_not_none(
            cube.dimension,
            "dimension",
            self.dimension,
        )
        hierarchy = check_named_object_not_none(
            dimension.hierarchy,
            "hierarchy",
            self.name,
        )
        return (
            [hierarchy.level.name]  # type: ignore[attr-defined]
            if hierarchy.level and hierarchy.level.type.value != "ALL"  # type: ignore[attr-defined]
            else []
        )

    @property
    @deprecated(
        "`Hierarchy.levels` is deprecated, iterate on the hierarchy instead.",
        category=_DEPRECATED_WARNING_CATEGORY,
    )
    def levels(self) -> Mapping[str, Level]:
        """Levels of the hierarchy.

        :meta private:
        """
        return {
            level_name: Level(
                LevelIdentifier(self._identifier, level_name),
                atoti_client=self._atoti_client,
                cube_identifier=self._cube_identifier,
                java_api=self._java_api,
            )
            for level_name in self._get_level_names(key=None)
        }

    @override
    def __getitem__(self, key: LevelName, /) -> Level:
        level_names = self._get_level_names(key=key)
        if not level_names:
            raise KeyError(key)
        assert len(level_names) == 1
        return Level(
            LevelIdentifier(self._identifier, level_names[0]),
            atoti_client=self._atoti_client,
            cube_identifier=self._cube_identifier,
            java_api=self._java_api,
        )

    @override
    def __iter__(self) -> Iterator[LevelName]:
        return iter(self._get_level_names(key=None))

    @override
    def __len__(self) -> int:
        return len(self._get_level_names(key=None))

    @property
    def name(self) -> HierarchyName:
        """Name of the hierarchy."""
        return self._identifier.hierarchy_name

    @property
    def _properties(self) -> MutableMapping[str, JsonValue]:
        return HierarchyProperties(
            cube_name=self._cube_identifier.cube_name,
            hierarchy_identifier=self._identifier,
            java_api=self._java_api,
        )

    @override
    def _repr_json_(self) -> ReprJson:
        root = f"{self.name}{' (slicing)' if self.slicing else ''}"
        return (
            list(self),
            {
                "root": root,
                "expanded": False,
            },
        )

    @property
    def slicing(self) -> bool:
        """Whether the hierarchy is slicing or not.

        * A regular (i.e. non-slicing) hierarchy is considered aggregable, meaning that it makes sense to aggregate data across all members of the hierarchy.

          For instance, for a :guilabel:`Geography` hierarchy, it is useful to see the worldwide aggregated :guilabel:`Turnover` across all countries.

        * A slicing hierarchy is not aggregable at the top level, meaning that it does not make sense to aggregate data across all members of the hierarchy.

          For instance, for an :guilabel:`As of date` hierarchy giving the current bank account :guilabel:`Balance` for a given date, it does not provide any meaningful information to aggregate the :guilabel:`Balance` across all the dates.
        """
        # Remove `not self._java_api` once query sessions are supported.
        if not self._java_api or not self._atoti_client._graphql_client:
            cube_discovery = self._atoti_client.get_cube_discovery()
            return (
                cube_discovery.cubes[self._cube_identifier.cube_name]
                .name_to_dimension[self.dimension]
                .name_to_hierarchy[self.name]
                .slicing
            )

        data_model_transaction_id = get_data_model_transaction_id()

        output = self._atoti_client._graphql_client.get_hierarchy_is_slicing(
            cube_name=self._cube_identifier.cube_name,
            dimension_name=self.dimension,
            hierarchy_name=self.name,
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
        dimension = check_named_object_not_none(
            cube.dimension,
            "dimension",
            self.dimension,
        )
        hierarchy = check_named_object_not_none(
            dimension.hierarchy,
            "hierarchy",
            self.name,
        )
        return hierarchy.is_slicing

    @slicing.setter
    def slicing(self, value: bool, /) -> None:
        java_api = require_live_extension(self._java_api)
        java_api.update_hierarchy_slicing(
            self._identifier,
            value,
            cube_name=self._cube_identifier.cube_name,
        )
        java_api.refresh()

    @property
    @doc(
        cardinality_threshold=str(_VIRTUAL_HIERARCHY_CARDINALITY_THRESHOLD),
        force_property_name=_FORCE_VIRTUAL_PROPERTY_NAME,
    )
    def virtual(self) -> bool | None:
        r"""Whether the hierarchy is virtual or not.

        A virtual hierarchy does not store in memory the list of its members.
        Hierarchies with large cardinality are good candidates for being virtual.

        By default, a given hierarchy is automatically set as virtual if and only if it comes from an :class:`~atoti.ExternalTable` and one of the following conditions is met:

        * The hierarchy has a cardinality of {cardinality_threshold} or more;
        * The ``{force_property_name}`` property is set to ``true``.

        Note:
            As its name suggests, ``{force_property_name}`` is an experimental/temporary property which may change in future bugfix releases.

        Example:
            .. doctest::
                :hide:

                >>> clickhouse_server_port = getfixture("clickhouse_server_port")
                >>> schema_name = "tck_db_v1"

            >>> from atoti_directquery_clickhouse import ConnectionConfig, TableConfig
            >>> connection_config = ConnectionConfig(
            ...     url=f"clickhouse:http://localhost:{{clickhouse_server_port}}/{{schema_name}}",
            ... )
            >>> table_config = TableConfig(keys={{"id"}})

            * Without ``{force_property_name}``:

              >>> session = tt.Session.start()
              >>> external_database = session.connect_to_external_database(
              ...     connection_config
              ... )
              >>> sales_table = session.add_external_table(
              ...     external_database.tables["sales"], config=table_config
              ... )
              >>> cube = session.create_cube(sales_table)
              >>> cube.hierarchies["product"].virtual
              False

            * With ``{force_property_name}``:

              >>> session_config = tt.SessionConfig(
              ...     java_options=["-D{force_property_name}=true"]
              ... )
              >>> session = tt.Session.start(session_config)
              >>> external_database = session.connect_to_external_database(
              ...     connection_config
              ... )
              >>> sales_table = session.add_external_table(
              ...     external_database.tables["sales"], config=table_config
              ... )
              >>> cube = session.create_cube(sales_table)
              >>> cube.hierarchies["product"].virtual
              True

            .. doctest::
                :hide:

                >>> ASqlDatabaseManager = session._java_api.jvm.io.atoti.runtime.private_.directquery.sql.ASqlDatabaseManager
                >>> assert (
                ...     int("{cardinality_threshold}")
                ...     == ASqlDatabaseManager.VIRTUAL_HIERARCHY_LIMIT
                ... )
                >>> assert (
                ...     "{force_property_name}"
                ...     == ASqlDatabaseManager.FORCE_VIRTUAL_HIERARCHIES_PROPERTY
                ... )
                >>> del session
        """
        # Remove `not self._java_api` once query sessions are supported.
        if not self._java_api or not self._atoti_client._graphql_client:
            return None

        data_model_transaction_id = get_data_model_transaction_id()

        output = self._atoti_client._graphql_client.get_hierarchy_is_virtual(
            cube_name=self._cube_identifier.cube_name,
            data_model_transaction_id=data_model_transaction_id,
            dimension_name=self.dimension,
            hierarchy_name=self.name,
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
        dimension = check_named_object_not_none(
            cube.dimension,
            "dimension",
            self.dimension,
        )
        hierarchy = check_named_object_not_none(
            dimension.hierarchy,
            "hierarchy",
            self.name,
        )
        return hierarchy.is_virtual

    @virtual.setter
    def virtual(self, virtual: bool, /) -> None:
        java_api = require_live_extension(self._java_api)
        java_api.update_hierarchy_virtual(
            self._identifier,
            virtual,
            cube_name=self._cube_identifier.cube_name,
        )
        java_api.refresh()

    @property
    def visible(self) -> bool:
        """Whether the hierarchy is visible or not."""
        # Remove `not self._java_api` once query sessions are supported.
        if not self._java_api or not self._atoti_client._graphql_client:
            cube_discovery = self._atoti_client.get_cube_discovery()
            return (
                cube_discovery.cubes[self._cube_identifier.cube_name]
                .name_to_dimension[self.dimension]
                .name_to_hierarchy[self.name]
                .visible
            )

        data_model_transaction_id = get_data_model_transaction_id()

        output = self._atoti_client._graphql_client.get_hierarchy_is_visible(
            cube_name=self._cube_identifier.cube_name,
            data_model_transaction_id=data_model_transaction_id,
            dimension_name=self.dimension,
            hierarchy_name=self.name,
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
        dimension = check_named_object_not_none(
            cube.dimension,
            "dimension",
            self.dimension,
        )
        hierarchy = check_named_object_not_none(
            dimension.hierarchy,
            "hierarchy",
            self.name,
        )
        return hierarchy.is_visible

    @visible.setter
    def visible(self, value: bool, /) -> None:
        def update_input(update_hierarchy_input: UpdateHierarchyInput, /) -> None:
            update_hierarchy_input.is_visible = value

        self._update(update_input)

    @property
    def members_indexed_by_name(self) -> bool:
        """Whether the hierarchy maintains an index of its members by name.

        :meta private:
        """
        graphql_client = require_live_extension(self._atoti_client._graphql_client)
        data_model_transaction_id = get_data_model_transaction_id()

        output = graphql_client.get_hierarchy_are_members_indexed_by_name(
            cube_name=self._cube_identifier.cube_name,
            data_model_transaction_id=data_model_transaction_id,
            dimension_name=self.dimension,
            hierarchy_name=self.name,
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
        dimension = check_named_object_not_none(
            cube.dimension,
            "dimension",
            self.dimension,
        )
        hierarchy = check_named_object_not_none(
            dimension.hierarchy,
            "hierarchy",
            self.name,
        )
        return hierarchy.are_members_indexed_by_name

    @members_indexed_by_name.setter
    def members_indexed_by_name(self, value: bool, /) -> None:
        def update_input(update_hierarchy_input: UpdateHierarchyInput, /) -> None:
            update_hierarchy_input.are_members_indexed_by_name = value

        self._update(update_input)

    def _update(self, update_input: Callable[[UpdateHierarchyInput], None], /) -> None:
        graphql_client = require_live_extension(self._atoti_client._graphql_client)
        data_model_transaction_id = get_data_model_transaction_id()

        mutation_input = UpdateHierarchyInput(
            cube_name=self._cube_identifier.cube_name,
            data_model_transaction_id=data_model_transaction_id,
            hierarchy_identifier=self._identifier._graphql_input,
        )
        update_input(mutation_input)

        graphql_client.update_hierarchy(mutation_input)
