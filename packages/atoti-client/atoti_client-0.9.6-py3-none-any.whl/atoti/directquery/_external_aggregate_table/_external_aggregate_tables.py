from collections.abc import Mapping, Set as AbstractSet
from typing import Final, final

from typing_extensions import override

from ..._collections import DelegatingMutableMapping
from ..._java_api import JavaApi
from ..._require_live_extension import require_live_extension
from .external_aggregate_table import ExternalAggregateTable


@final
class ExternalAggregateTables(DelegatingMutableMapping[str, ExternalAggregateTable]):
    def __init__(self, *, java_api: JavaApi | None):
        self._java_api: Final = java_api

    @override
    def _get_delegate(self, *, key: str | None) -> Mapping[str, ExternalAggregateTable]:
        java_api = require_live_extension(self._java_api)
        return java_api.get_external_aggregate_tables(key=key)

    @override
    def _update_delegate(self, other: Mapping[str, ExternalAggregateTable], /) -> None:
        java_api = require_live_extension(self._java_api)
        new_mapping = {**self}
        new_mapping.update(other)
        java_api.set_external_aggregate_tables(new_mapping)
        java_api.refresh()

    @override
    def _delete_delegate_keys(self, keys: AbstractSet[str], /) -> None:
        java_api = require_live_extension(self._java_api)
        java_api.remove_external_aggregate_tables(keys)
        java_api.refresh()
