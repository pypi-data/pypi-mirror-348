from collections.abc import Set as AbstractSet
from typing import Final, final

from typing_extensions import override

from .._atoti_client import AtotiClient
from .._base_scenario_name import BASE_SCENARIO_NAME as _BASE_SCENARIO_NAME
from .._check_not_none import (
    check_data_model_not_none,
    check_named_object_not_none,
)
from .._constant import Scalar
from .._graphql_client import UnloadMembersFromDataCubeInput
from .._identification import (
    HasIdentifier,
    Identifiable,
    LevelIdentifier,
    QueryCubeIdentifier,
    QueryCubeName,
    identify,
)
from .._ipython import ReprJson, ReprJsonable
from .._java_api import JavaApi
from .._require_live_extension import require_live_extension
from .._transaction import get_data_model_transaction_id


# Only add methods and properties to this class if they are specific to query cubes.
# See comment in `BaseSession` for more information.
@final
class QueryCube(HasIdentifier[QueryCubeIdentifier], ReprJsonable):
    r"""A query cube of a :class:`~atoti.QuerySession`."""

    def __init__(
        self,
        identifier: QueryCubeIdentifier,
        /,
        *,
        atoti_client: AtotiClient,
        java_api: JavaApi | None,
    ):
        self._atoti_client: Final = atoti_client
        self.__identifier: Final = identifier
        self._java_api: Final = java_api

    @property
    @override
    def _identifier(self) -> QueryCubeIdentifier:
        return self.__identifier

    @property
    def name(self) -> QueryCubeName:
        """The name of the query cube."""
        return self._identifier.cube_name

    @property
    def distributing_levels(self) -> AbstractSet[LevelIdentifier]:
        """The identifiers of the levels distributing data across the data cubes connecting to the query cube.

        Each level is independently considered as a partitioning key.
        This means that for a query cube configured with ``distributing_levels={date_level_key, region_level_key}``, each data cube must contribute a unique :guilabel:`date`, not present in any other data cube, as well as a unique :guilabel:`region`.
        """
        java_api = require_live_extension(self._java_api)
        levels = java_api.get_distributing_levels(self._identifier)
        return frozenset(
            LevelIdentifier._parse_java_description(level_description)
            for level_description in levels
        )

    @property
    def data_cube_ids(self) -> AbstractSet[str]:
        """Opaque IDs representing each data cubes connected to this query cube."""
        graphql_client = require_live_extension(self._atoti_client._graphql_client)
        data_model_transaction_id = get_data_model_transaction_id()

        output = graphql_client.get_cluster_members(
            cube_name=self.name, data_model_transaction_id=data_model_transaction_id
        )
        data_model = check_data_model_not_none(
            output.data_model,
            data_model_transaction_id=data_model_transaction_id,
        )
        query_cube = check_named_object_not_none(
            data_model.cube,
            "query cube",
            self.name,
        )
        return (
            frozenset()
            if query_cube.cluster is None
            else frozenset(node.name for node in query_cube.cluster.nodes)
        )

    def unload_members_from_data_cube(
        self,
        members: AbstractSet[Scalar],
        *,
        data_cube_id: str,
        level: Identifiable[LevelIdentifier],
        scenario_name: str = _BASE_SCENARIO_NAME,
    ) -> None:
        """Unload the given members of a level from a data cube.

        This is mostly used for data rollover.

        Note:
            This requires the query cube to have been created with :attr:`~atoti.QueryCubeDefinition.allow_data_duplication` set to ``True`` and with non empty :attr:`~atoti.QueryCubeDefinition.distributing_levels`.

        Args:
            members: The members to unload.
            data_cube_id: The ID of the data cube from which to unload the members.
                This must be equal to the *id_in_cluster* argument passed to :meth:`~atoti.Session.create_cube`.
            level: The level containing the members to unload.
            scenario_name: The name of the scenario from which facts must unloaded.

        Example:
            .. doctest::
                :hide:

                >>> from secrets import token_urlsafe
                >>> from tempfile import mkdtemp
                >>> from time import sleep
                >>> import pandas as pd
                >>> from atoti_jdbc import JdbcPingDiscoveryProtocol

            Setting up the cubes:

            >>> query_session = tt.QuerySession.start()
            >>> data_session = tt.Session.start()
            >>> def query_by_city():
            ...     cube = query_session.session.cubes["Query cube"]
            ...     l, m = cube.levels, cube.measures
            ...     return cube.query(m["Number.SUM"], levels=[l["City"]])
            >>> def wait_for_data(*, expected_city_count: int):
            ...     max_attempts = 30
            ...     for _ in range(max_attempts):
            ...         try:
            ...             if len(query_by_city().index) == expected_city_count:
            ...                 return
            ...         except:
            ...             pass
            ...         sleep(1)
            ...     raise RuntimeError(f"Failed {max_attempts} attempts.")
            >>> data_session.clusters["Cluster"] = query_session.session.clusters[
            ...     "Cluster"
            ... ] = tt.ClusterDefinition(
            ...     application_names={"Cities"},
            ...     discovery_protocol=JdbcPingDiscoveryProtocol(
            ...         f"jdbc:h2:{mkdtemp('atoti-cluster')}/db",
            ...         username="sa",
            ...         password="",
            ...     ),
            ...     authentication_token=token_urlsafe(),
            ... )
            >>> query_session.query_cubes["Query cube"] = tt.QueryCubeDefinition(
            ...     query_session.session.clusters["Query cube"],
            ...     application_names={"Cities"},
            ...     allow_data_duplication=True,
            ...     distributing_levels={("Cities", "City", "City")},
            ... )
            >>> data = pd.DataFrame(
            ...     columns=["City", "Number"],
            ...     data=[
            ...         ("Paris", 20.0),
            ...         ("London", 5.0),
            ...         ("NYC", 7.0),
            ...     ],
            ... )
            >>> table = data_session.read_pandas(
            ...     data, keys={"City"}, table_name="Cities"
            ... )
            >>> data_cube = data_session.create_cube(table, id_in_cluster="Europe")
            >>> wait_for_data(expected_city_count=3)
            >>> query_by_city()
                   Number.SUM
            City
            London       5.00
            NYC          7.00
            Paris       20.00

            Unloading the facts associated with the :guilabel:`London` and :guilabel:`NYC` members:

            >>> query_cube = query_session.query_cubes["Query cube"]
            >>> query_cube.unload_members_from_data_cube(
            ...     {"London", "NYC"},
            ...     data_cube_id="Europe",
            ...     level=data_cube.levels["City"],
            ... )
            >>> wait_for_data(expected_city_count=1)
            >>> query_by_city()
                  Number.SUM
            City
            Paris      20.00

        """
        graphql_client = require_live_extension(self._atoti_client._graphql_client)
        mutation_input = UnloadMembersFromDataCubeInput(
            branch_name=scenario_name,
            data_cube_id=data_cube_id,
            level_identifier=identify(level)._graphql_input,
            members=list(members),
            query_cube_name=self.name,
        )
        graphql_client.unload_members_from_data_cube(mutation_input)

    @override
    def _repr_json_(self) -> ReprJson:
        return (
            {"name": self.name},
            {"expanded": False, "root": self.name},
        )
