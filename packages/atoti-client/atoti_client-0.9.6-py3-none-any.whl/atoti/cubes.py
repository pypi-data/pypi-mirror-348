from collections.abc import Callable, Mapping, Set as AbstractSet
from typing import Final, final

from typing_extensions import override

from ._atoti_client import AtotiClient
from ._check_not_none import check_data_model_not_none
from ._collections import DelegatingConvertingMapping, SupportsUncheckedMappingLookup
from ._cube_definition import CubeDefinition
from ._identification import CubeIdentifier, CubeName, identify
from ._ipython import ReprJson, ReprJsonable
from ._java_api import JavaApi
from ._require_live_extension import require_live_extension
from ._transaction import get_data_model_transaction_id
from .cube import Cube


@final
class Cubes(
    SupportsUncheckedMappingLookup[CubeName, CubeName, Cube],
    DelegatingConvertingMapping[CubeName, CubeName, Cube, CubeDefinition],
    ReprJsonable,
):
    r"""Manage the :class:`~atoti.Cube`\ s of a :class:`~atoti.Session`."""

    def __init__(
        self,
        *,
        atoti_client: AtotiClient,
        get_widget_creation_code: Callable[[], str | None],
        java_api: JavaApi | None,
        session_id: str,
    ) -> None:
        self._atoti_client: Final = atoti_client
        self._get_widget_creation_code: Final = get_widget_creation_code
        self._java_api: Final = java_api
        self._session_id: Final = session_id

    @override
    def _create_lens(self, key: CubeName, /) -> Cube:
        return Cube(
            CubeIdentifier(key),
            atoti_client=self._atoti_client,
            get_widget_creation_code=self._get_widget_creation_code,
            java_api=self._java_api,
            session_id=self._session_id,
        )

    @override
    def _get_unambiguous_keys(self, *, key: CubeName | None) -> list[CubeName]:
        # Remove `not self._java_api` once query sessions are supported.
        if not self._java_api or not self._atoti_client._graphql_client:
            cube_discovery = self._atoti_client.get_cube_discovery()
            return [
                cube_name
                for cube_name in cube_discovery.cubes
                if key is None or cube_name == key
            ]

        data_model_transaction_id = get_data_model_transaction_id()

        if key is None:
            output = self._atoti_client._graphql_client.get_cubes(
                data_model_transaction_id=data_model_transaction_id
            )
            data_model = check_data_model_not_none(
                output.data_model,
                data_model_transaction_id=data_model_transaction_id,
            )
            return [cube.name for cube in data_model.cubes]

        output = self._atoti_client._graphql_client.find_cube(  # type: ignore[assignment] # See https://github.com/python/mypy/issues/12968.
            cube_name=key, data_model_transaction_id=data_model_transaction_id
        )
        data_model = check_data_model_not_none(
            output.data_model,
            data_model_transaction_id=data_model_transaction_id,
        )
        cube = data_model.cube  # type: ignore[attr-defined]
        return [] if cube is None else [cube.name]

    @override
    def _update_delegate(
        self,
        other: Mapping[CubeName, CubeDefinition],
        /,
    ) -> None:
        java_api = require_live_extension(self._java_api)

        for name, definition in other.items():
            java_api.create_cube_from_table(
                name,
                application_name=name
                if definition.application_name is None
                else (definition.application_name or None),
                catalog_names=definition.catalog_names,
                filter=definition.filter,
                mode=definition._mode,
                table_identifier=identify(definition.fact_table),
                id_in_cluster=definition.id,
                priority=definition.priority,
            )
        java_api.refresh()

        if java_api.get_readiness():
            for name in other:
                # AutoJoin distributed clusters if the session has been marked as ready
                java_api.auto_join_distributed_clusters(cube_name=name)
            java_api.refresh()

    @override
    def _delete_delegate_keys(self, keys: AbstractSet[CubeName], /) -> None:
        java_api = require_live_extension(self._java_api)
        for key in keys:
            java_api.delete_cube(key)

    @override
    def _repr_json_(self) -> ReprJson:
        """Return the JSON representation of cubes."""
        return (
            {name: cube._repr_json_()[0] for name, cube in sorted(self.items())},
            {"expanded": False, "root": "Cubes"},
        )
